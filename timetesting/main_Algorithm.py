##This program takes as input:
# *steps which includes t_list(s) and gates 
# *c_ops
# *anharmonicity
# * psi0_start ? (number of qubits qubits and energy levels are the important things, all qubits are assumed to be in ground state)
# * envelope fcn
##This program calls a function which performs the #gate algorithm"
##THis program should return the final state
from qutip import *
import numpy as np
import GateFuncs as gf
import mcsolving
from Anharmonicity import anharmonicity

def main_algorithm(args):
    """ The main algorithm.
    Takes in args:
    steps of the algorithm containing information
    about gates, collapes operators, initial state, list of Qubit objects and
    anharmonicity strength (and maybe ntraj?).
    What it does:
    It first converts the first step of the
    algorithm steps to a Hamiltonian, with anharmonicity. Then runs the first mcsolve
    with 'ntraj' trajectories. This returns an array (converted to list) of final states.
    It then goes to a parfor loop over the remaining steps which runs mcsolve with 1
    trajectory for each of these final states. This is done to be able to apply
    virtual gates after every step of the algorithm, and to be able to continue
    each trajectory where it left off in the last step without risking errors that
    could come from taking average states and so on
    What it returns:
    The function returns a list (of length ntraj) of the final states"""
    steps = args["steps"]
    c_ops = args["c_ops"]
    psi0 = args["psi0"]
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    t_st = [0]
    t = 0
    td = []
    tmaxarray = []
    physicalgatesarray = []

    H = anharmonicity(Qblist) # + ZZ_Interaction(Qblist)
    ## Do first iteration for ntraj trajectories to split the mcsolve
    for step in steps:
        physicalgates, virtualgates, tmax, tdrive = gf.CreateHfromStep(step, Qblist, t_max)  # gates contains physical gates, virtual gates, t_max, IN THAT ORDER
        td.append(tdrive)
        t += tdrive
        t_st.append(t)
        tmaxarray.append(tmax)
        physicalgatesarray.append(physicalgates)
    tlist = np.linspace(0,t,10*len(steps)) #Eventuellt kör bara med 10.
    del t_st[-1]
    #print(t)
    #print(td)
    #print(t_st)
    for i in range(len(steps)):
        Htd = gf.TimeDepend(steps[i], physicalgatesarray[i], td[i], Qblist, t_st[i], tlist, tmaxarray[i])
        H = Htd + H
    if max(tlist) >= 1e-11:  # If the tlist is too small we get integration error
        if c_ops != []:
            output = mcsolve(H, psi0, tlist, c_ops=c_ops, ntraj=ntraj, progress_bar=None)
            psi0 = output.states[:, -1].tolist()
        else:
            output = sesolve(H, psi0, tlist, e_ops=[])
            psi0 = [Qobj(output.states[-1])] #If all noise rates=0, we use sesolve instead of mcsolve => only one state
    #for vgate in virtualgates:
    #    psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
    ''' I don't know if we want to have the possibility to run with no noise.. but now we do.. 
    just remove the if statements if we want to remove. Maybe it slows it down, it's before the loops so its probably ok
    '''
    """
    if c_ops != []:
        for i in range(1,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if max(tlist) >= 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
            for vgate in virtualgates:
                psi0= parfor(mcsolving.virtgate, psi0, vgate=vgate)
    else:
        for i in range(1,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if max(tlist) > 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
            for vgate in virtualgates:
                psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
    """
    return psi0

