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
    """ The main algorithm. Takes in args: steps of the algorithm containing information
    about gates, collapes operators, initial state, list of Qubit objects and
    anharmonicity strength (and maybe ntraj?). It first converts the first step of the
    algorithm steps to a Hamiltonian, with anharmonicity. Then runs the first mcsolve
    with 'ntraj' trajectories. This returns an array (converted to list) of final states.
    It then goes to a parfor loop over the remaining steps which runs mcsolve with 1
    trajectory for each of these final states. This is done to be able to apply
    virtual gates after every step of the algorithm, and to be able to continue
    each trajectory where it left off in the last step without risking errors that
    could come from taking average states and so on
    The function returns a list of the final states"""
    steps = args["steps"]
    c_ops = args["c_ops"]
    psi0 = args["psi0"]
    Qblist = args["Qblist"]
    U = args["U"]
    if "ntraj" in args:
        ntraj = args["ntraj"]
    else:
        ntraj = 500

    H0 = anharmonicity(U, Qblist) # + ZZ_Interaction(Qblist)

    ## Do first iteration for ntraj trajectories to split the mcsolve
    gates = gf.CreateHfromStep(steps[0], Qblist)  # gates contains physical gates, virtual gates, t_max, IN THAT ORDER
    H = gf.TimeDepend(steps[0], gates[0], gates[2])[0] + H0
    virtualgate = gates[1]
    tlist = gf.TimeDepend(steps[0], gates[0], gates[2])[1]
    output = mcsolve(H, psi0, tlist, c_ops=c_ops, ntraj=ntraj)
    psi0 = output.states[:, -1].tolist()

    for i in range(1,len(steps)): #each step except the first one
        gates = gf.CreateHfromStep(steps[i], Qblist)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
        H = gf.TimeDepend(steps[i], gates[0], gates[2])[0] + H0
        virtualgate = gates[1]
        tlist = gf.TimeDepend(steps[i], gates[0], gates[2])[1]
        psi_temp = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
        psi0 = psi_temp
    return psi0
    
