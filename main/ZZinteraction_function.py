import numpy as np
from qutip import *
import Qb_class as qc

""""Problem: if we have sigmaz_1 * sigmaz_2 with dimensional mismatch, its not gonna work."""


def ZZ_interaction(Qblist):
    eye_vec = []
    H_intlist = []
    H_interaction = 0
    inter = 0

    for QB in enumerate(Qblist):  #creates array of identity matrices of correct dimensions
        eye_vec.append(qeye(QB[1].level))

    for qb in enumerate(Qblist): #enumerates through array of Qubits and creates interaction operators qubits that interacts
        eyeqb = eye_vec.copy()

        if qb[1].noisert_vec[2] > 0.0: # checks to see if there is any noise and adds sigmaz for qubit
            eyeqb[qb[0]] = destroy(qb[1].level).dag() * destroy(qb[1].level)

            for q in enumerate(Qblist): #checks to see which qubits that the qubits interacts with
                eyeq = eye_vec.copy()

                if 0.0 < np.sqrt((q[1].desig[0] - qb[1].desig[0]) ** 2 + (q[1].desig[1] - qb[1].desig[1]) ** 2) < 1.0:
                    eyeq[q[0]] = destroy(q[1].level).dag() * destroy(q[1].level)
                    inter = inter + qb[1].noisert_vec[2] * tensor(eyeqb) * tensor(eyeq)
                    H_intlist.append(inter)

    for ind in range(0, len(H_intlist)): #adds interaction terms together and returns hamiltonian term for ZZ-interaction
        H_interaction = H_interaction + H_intlist[ind]

        ind += ind

    return H_interaction

