from qutip import *

def anharmonicity(Qblist):
    """function for creating anharmonicty term for the Hamiltonian.
    Qblist[i].Anharm = U (anharmonicity freq) for the i:th qubit
    'Anharm' function tensors the gate out correctly """
    H = 0
    for i in range(len(Qblist)):
        H = H + Qblist[i].anharm*AnHarm(Qblist, i)
    return H

def AnHarm(Qblist, target):
    """Creates anharmonicity term of correct dimension
    Input is list of qubits and which qubit you want to target with the operator
    Returns Qobj anharmonicity operator for the targeted qubit """
    AH = [qeye(Qb.level) for Qb in Qblist]
    AH[target] = create(Qblist[target].level)*create(Qblist[target].level)*destroy(Qblist[target].level)*destroy(Qblist[target].level)
    return tensor(AH)