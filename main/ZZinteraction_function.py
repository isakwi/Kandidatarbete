import numpy as np
from qutip import *
import Qb_class as qc

"""Creates ZZ-interaction term for hamiltonian , input is list fo qubits and interaction matrix containing interaction strength 
between qubits, returns term for hamiltonian"""








def ZZ_interaction(Qblist, interaction_mat):
    eye_vec = []
    H_intlist = []
    H_interaction = 0
    inter = 0

    for QB in enumerate(Qblist):  #creates array of identity matrices of correct dimensions
        eye_vec.append(qeye(QB[1].level))

    for qb in enumerate(Qblist): #enumerates through array of Qubits and creates interaction operators qubits that interacts
        eyeqb = eye_vec.copy()
        eyequb = eye_vec.copy()

        for qub in enumerate(Qblist):
            if interaction_mat[qb[0], qub[0]] > 0 and qb[0] != qub[0]:
                eyeqb[qb[0]] = destroy(qb[1].level).dag() * destroy(qb[1].level)
                eyequb[qub[0]] = destroy(qub[1].level).dag() * destroy(qub[1].level)

                inter = inter + interaction_mat[qb[0],qub[0]] * tensor(eyeqb)*tensor(eyequb)
                H_intlist.append(inter)

    for ind in range(0, len(H_intlist)): #adds interaction terms together and returns hamiltonian term for ZZ-interaction
        H_interaction = H_interaction + H_intlist[ind]

        ind += ind

    return H_interaction


