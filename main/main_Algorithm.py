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


##--------EVERYTHING ABOVE THIS IS JUST TAKING IN INPUT
def main_algorithm(args):
    steps = args["steps"]
    c_ops = args["c_ops"]
    psi0 = args["psi0"]
    if "ntraj" in args:
        ntraj = args["ntraj"]
    else:
        ntraj = 500
    H0 = ZZ_Interaction(Qblist) + anharmonicity(Qblist)
    for i in range(len(steps)): #each 
        gates = gate_algorithm(steps[i], Qblist) #gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
        H = gates[0] +  H0
        virtualgate = gates[1]
        tlist = gates[2]
        output = mcsolve(H,psi0, tlist, c_ops = c_ops, ntraj = ntraj)
        psi0 = output.states[-1]
        #the virtual gates should be able to apply through matrix multiplication
        if virtualgate != None:
            psi0 = virtualgates[i] * psi0
    return psi0
    
