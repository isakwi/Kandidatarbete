from qutip import *
from .GateLib import AnHarm

def anharmonicity(Qblist):
    """function for creating anharmonicty term for the Hamiltonian.
    Qblist[i].anharm = U for the i:th qubit
    'Anharm' in GateLib tensors the gate out correctly """
    H = 0
    for i in range(len(Qblist)):
        H = H + Qblist[i].anharm*AnHarm(Qblist, i)
    return H
