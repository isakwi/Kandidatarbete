from qutip import *


def anharmonicity(U, Qblist):
    #function for creating the anharmonicty term for the Hamiltonian. 
    H = []
    for i in range(0, len(Qblist)):
        a_i = destroy(Qblist[i].level)
        H_i = U * a_i.dag() * a_i.dag() * a_i * a_i
        H.append(H_i)
    return H
