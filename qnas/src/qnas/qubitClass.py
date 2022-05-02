__all__ = ['Qubit', 'createPsi0']


from qutip import basis, tensor

class Qubit:
    """ Definition of Qubit object class
    Includes:
    - level = qubit levels (eg 2, 3 or 4)
    - noisert_vec = list of noise rates [relaxation, dephasing, excitation]
    - anharm = anharmonicity value for the qubit """
    def __init__(self, level, noisert_vec, anharm):
        self.level = level
        self.noisert_vec = noisert_vec
        self.anharm = anharm


def createPsi0(Qblist, init_state):
    """ Creates initial state with correct dimensions
    Input:
    - Qblist = list of Qubit objects
    - init_state = int of initial state value (often =0)"""
    psi0 = [basis(Qb.level, init_state) for Qb in Qblist]
    return tensor(psi0)

