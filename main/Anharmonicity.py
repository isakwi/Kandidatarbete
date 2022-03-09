from qutip import *
from GateLib import AnHarm

def anharmonicity(U, Qblist):
    #function for creating the anharmonicty term for the Hamiltonian. 
    H = 0
    for i in range(len(Qblist)):
        H = H + U*AnHarm(Qblist, i)
    return H
