
import Qb_class as Qb
from qutip import *
import numpy as np
import GateLib
import sys



def TensorifyExpectationOperator(Qblist, Tar_Con, Gate):
    """
    Tensors out gates for which to calculate the expectation values.
    Inputs are:
    Qblist,
    Tar_Con = int for 1qb gates, and list [i,j] for 2qb gates
    Gate = Qobj of dimensions corresponding to the targeted qubit levels. (N x N) if qubit.level = N
    """
    gateList = [qeye(Qb.level) for Qb in Qblist]
    if type(Tar_Con) == int:  # 1qb gate
        gateList[Tar_Con] = Gate
        if Gate.shape[0] != Qblist[Tar_Con].level:
            print('Error: Shape of e_ops doesn\'t match the targeted qubit level. \n See \'GateLib\' for more info')
            sys.exit(1)
        return tensor(gateList)
    elif len(Tar_Con) == 2: # 2qb gate
        if Gate.shape[0] != Qblist[Tar_Con[0]].level*Qblist[Tar_Con[1]].level:
            print('Error: Shape of e_ops doesn\'t match the targeted qubits levels. \n See \'GateLib\' for more info')
            sys.exit(1)
        return GateLib.gate_expand_2toN(Gate, len(Qblist), gateList, Tar_Con[1],Tar_Con[0])
    else:
        print('Error: QnAS only handles 1 or 2 qubit operators as e_ops. \n See \'GateLib\' for more info')
        sys.exit(1)  # Stops the program with the same error code as above
        # Kan nog fixa mer allmänna också...

def CreateE_opsList(Qblist, e_ops_inp):
    """
    Input given on the form:
    e_ops_inp = [[e_op1, Tar_Con],
                 [e_op2, Tar_Con], ... ]
    where e_op is a Qobj with the dimensions  ( qubit.level x qubit.level )
    and Tar_Con is the target and control in case of 2qb gate, as before.
    """
    e_ops=[]
    for i in range(len(e_ops_inp)):
        e_ops.append(TensorifyExpectationOperator(Qblist, e_ops_inp[i][1], e_ops_inp[i][0]))
    return e_ops


def main_algorithm(args): #This is for when we have e_ops. This is just copied from main_Alg_parfortest.py, nothing changed yet
    steps = args["steps"]
    c_ops = args["c_ops"]
    init_state = args["psi0"]
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    StoreTimeDynamics = args["StoreTimeDynamics"]
    tlist_tot = [0]
    e_ops = args["e_ops"]
    expectvals = 0 # Write over this later

    psi0 = []
    for i in range(ntraj):
        psi0.append(init_state)

    H0 = anharmonicity(Qblist) # + ZZ_Interaction(Qblist)
    if c_ops != []:
        for i in range(0,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if StoreTimeDynamics:
                if steps[i].name[0] in ["VPZ"]:  # Check if VPZ step, then no time added to tlist
                    tlist_shifted = []
                else:
                    tlist_shifted = tlist + tlist_tot[-1] # Shifting the tlist to start where previous starts.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted )) # Create tlist for the entire process
            if max(tlist) >= 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops)
            for vgate in virtualgates:
                psi0= parfor(mcsolving.virtgate, psi0, vgate=vgate)
    else:
        for i in range(0,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if StoreTimeDynamics:
                if steps[i].name[0] in ["VPZ"]:  # Check if VPZ step, then no time added to tlist
                    tlist_shifted = []
                else:
                    tlist_shifted = tlist + tlist_tot[-1] # Shifting the tlist to start where previous starts.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted )) # Create tlist for the entire process
            if max(tlist) > 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=[])
            for vgate in virtualgates:
                psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
    if StoreTimeDynamics:
        tlist_tot = np.delete(tlist_tot, 0) # We get double zero in the beginning from tlist_tot = [0] initially
        return psi0, expectvals, tlist_tot
    else:
        return psi0
    
