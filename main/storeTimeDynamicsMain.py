
import qubitClass as Qb
from qutip import *
import numpy as np
import gateLib
import sys
import gateFuncs as gf
import mcSolving
from anharmonicity import anharmonicity
import zzInteractionFunction as zz


def tensorifyExpectationOperator(Qblist, Tar_Con, Gate):
    """
    Tensors out gates for which to calculate the expectation values.
    Inputs:
    - Qblist (list of Qubit objects)
    - Tar_Con = int for 1qb gates, and list [i,j] for 2qb gates. Which gate to target
    - Gate = Qobj of dimensions corresponding to the targeted qubit levels. (N x N) if qubit.level = N
    Output: Tensored gate with correct dimension
    """
    gateList = [qeye(Qb.level) for Qb in Qblist]
    if type(Tar_Con) == int:  # 1qb gate
        gateList[Tar_Con] = Gate
        if Gate.shape[0] != Qblist[Tar_Con].level:
            print('Error: Shape of e_ops doesn\'t match the targeted qubit level. \n See \'storeTimeDynamics\' for more info')
            sys.exit(1)
        return tensor(gateList)
    elif len(Tar_Con) == 2: # 2qb gate
        if Gate.shape[0] != Qblist[Tar_Con[0]].level*Qblist[Tar_Con[1]].level:
            print('Error: Shape of e_ops doesn\'t match the targeted qubits levels. \n See \'storeTimeDynamics\' for more info')
            sys.exit(1)
        del (gateList[max(Tar_Con)])  # Make room for the gate
        del (gateList[min(Tar_Con)])  # Make room for the gate
        return gateLib.gate_expand_2toN(Gate, len(Qblist), gateList, Tar_Con[1],Tar_Con[0])
    else:
        print('Error: QnAS only handles 1 or 2 qubit operators as e_ops. \n See \'ExpectationValues\' for more info')
        sys.exit(1)  # Stops the program with the same error code as above

def createExpectOpsList(Qblist, e_ops_inp):
    """
    Input given on the form:
    e_ops_inp = [[e_op1, Tar_Con],
                 [e_op2, Tar_Con], ... ]
    where e_op is a Qobj with the dimensions  ( qubit.level x qubit.level )
    and Tar_Con is the target and control in case of 2qb gate, as before.
    output: List of expectation value operators (e_ops)
    """
    e_ops=[]
    for i in range(len(e_ops_inp)):
        e_ops.append(tensorifyExpectationOperator(Qblist, e_ops_inp[i][1], e_ops_inp[i][0]))
    return e_ops


def mainAlgorithmExpectation(args):
    """
    mainAlgorithm modified to incorporate the StoreTimeDynamics option, by giving output:
    -final state
    -tlist for the entire algorithm
    -expectation values for a user specified set of e_ops, at each time step in the tlist.
    See mainAlgorithm.py for more information
    """
    steps = args["steps"]
    c_ops = args["c_ops"]
    init_state = args["psi0"] # maybe we should change the input so we can write args["init_state"] instead
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    tlist_tot = [0]
    e_ops_inp = args["e_ops_inp"]
    allStates = np.array([])  # a list where all states are saved

    psi0 = []
    for i in range(ntraj):
        psi0.append(init_state)

    e_ops = createExpectOpsList(Qblist, e_ops_inp) # Construct the e_ops array from e_ops_input

    try:
        zz_mat = args["zz_mat"]
        H0 = anharmonicity(Qblist) + zz.zzInteraction(Qblist, zz_mat)
    except:  # if zz interactions not specified, we skip them
        H0 = anharmonicity(Qblist)

    if c_ops != []:
        for i in range(0, len(steps)):  # all steps
            physicalgates, virtualgates, tmax = gf.createGatesFromStep(steps[i], Qblist, t_max)
            Htd, tlist = gf.timeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            print(steps)
            # Create tlist for the entire process
            for j in range(len(steps[i].name)): # Deals with steps with multiple gates in them
                if gateLib.isVirtual(steps[i], j): #Check if gate is virtual, then no time added to tlist
                    tlist_shifted = []
                else:
                    tlist_shifted = tlist + tlist_tot[-1]  # Shifting the tlist to start where previous ends.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted))
            # TODO : KOLLA ATT DET HÄR VERKLIGEN BLIR RÄTT ^
            if max(tlist) >= 1e-11:
                allStates = np.append(allStates, np.transpose(parfor(mcSolving.mcsTimeDynamics, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops)))
                psi0 = allStates[-ntraj:]
            for vgate in virtualgates:
                psi0 = parfor(mcSolving.virtgate, psi0, vgate=vgate)
    else:
        for i in range(0, len(steps)):
            physicalgates, virtualgates, tmax = gf.createGatesFromStep(steps[i], Qblist, t_max)
            Htd, tlist = gf.timeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0

            if gateLib.isVirtual(steps, i):
                tlist_shifted = []
            else:
                tlist_shifted = tlist + tlist_tot[-1]  # Shifting the tlist to start where previous starts.
            tlist_tot = np.concatenate((tlist_tot, tlist_shifted))  # Create tlist for the entire process

            if max(tlist) > 1e-11:
                allStates = np.append(allStates, np.transpose(parfor(mcSolving.mcsTimeDynamics, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops)))
                psi0 = allStates[-ntraj:]
            for vgate in virtualgates:
                psi0 = parfor(mcSolving.virtgate, psi0, vgate=vgate)

    tlist_tot = np.delete(tlist_tot, 0)  # We get double zero in the beginning since tlist_tot = [0] initially

    """CALCULATE EXPECTATION VALUES FROM ALL STATES HERE """
    print(shape(allStates))
    allStates = np.reshape(allStates, (len(tlist_tot), ntraj))
    # TODO: Koolla på detta igen ^
    if type(e_ops) == list and type(e_ops[0] == Qobj):
        expectvals = [np.array([np.mean(expect(e, parallelStates)) for parallelStates in allStates]) for e in e_ops]
    else:
        raise Exception("e_ops needs to be a list of Qobj")

    return psi0, expectvals, tlist_tot
#    return finalstate, expectvals, [tlist_tot]
"""Added parenthesis to tlist_tot so that tlist_tot will be an 2D array gives a reasonable format for plotting 
(I got an error if I didn't have it, but maybe we can avoid it in the future) //Albin"""
