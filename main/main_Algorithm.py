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


##--------EVERYTHING ABOVE THIS IS JUST TAKING IN INPUT
def main_algorithm(args):
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
    gates = gf.CreateHfromStep(steps[0], Qblist)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
    H = gf.TimeDepend(steps[0], gates[0], gates[2])[0] + H0
    virtualgate = gates[1]
    tlist = gf.TimeDepend(steps[0], gates[0], gates[2])[1]
    output = mcsolve(H, psi0, tlist, c_ops=c_ops, ntraj=ntraj)
    psi0 = []
    for idx in range(len(output.states[:,-1])):
        psi0.append(output.states[idx,-1])

    for i in range(1,len(steps)): #each step except the first one
        gates = gf.CreateHfromStep(steps[i], Qblist)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
        H = gf.TimeDepend(steps[i], gates[0], gates[2])[0] + H0
        virtualgate = gates[1]
        tlist = gf.TimeDepend(steps[i], gates[0], gates[2])[1]
        psi_temp = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
        psi0 = psi_temp
    return psi0
    
