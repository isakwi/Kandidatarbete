__all__ = ['anharmonicity', 'AnHarm']

from qutip import create, destroy, qeye, tensor

def anharmonicity(Qblist):
    """function for creating anharmonicty term for the Hamiltonian.
    Qblist[i].Anharm = U (anharmonicity freq) for the i:th qubit
    'Anharm' function tensors the gate out correctly
    Input:
    -Qblist = list of Quubit objects
    Output: Anharmonicity term for the Hamiltonian"""
    H = 0
    for i in range(len(Qblist)):
        H = H + Qblist[i].anharm/2*AnHarm(Qblist, i)
    return H

def AnHarm(Qblist, target):
    """Creates anharmonicity term of correct dimension
    Input is list of qubits and which qubit you want to target with the operator
    Returns Qobj anharmonicity operator for the targeted qubit
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the gate
    Output: anharmonicity term for one of the qubits with correct dimensions"""
    AH = [qeye(Qb.level) for Qb in Qblist]
    AH[target] = create(Qblist[target].level)*create(Qblist[target].level)*destroy(Qblist[target].level)*destroy(Qblist[target].level)
    return tensor(AH)
