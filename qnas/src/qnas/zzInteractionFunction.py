__all__ = ['zzInteraction']

from numpy import array
from qutip import qeye, destroy, tensor

def zzInteraction(Qblist, interaction_mat):
    """Creates ZZ-interaction term for hamiltonian
    Inputs:
    - Qblist = list of Qubit objects
    - interaction_mat = symmetric matrix containing the coupling constants between qubits as off diagonal elements
    Outputs: Constant zz-interaction term for the Hamiltonian"""
    eye_vec = []
    H_intlist = []
    H_interaction = 0
    inter = 0

    if type(interaction_mat) == list:
        interaction_mat = array(interaction_mat)
    for QB in enumerate(Qblist):  #creates array of identity matrices of correct dimensions
        eye_vec.append(qeye(QB[1].level))

    for qb in enumerate(Qblist): #enumerates through array of Qubits and creates interaction operators qubits that interacts
        eyeqb = eye_vec.copy()
        eyequb = eye_vec.copy()

        for qub in enumerate(Qblist):
            if interaction_mat[qb[0], qub[0]] > 0 and qb[0] != qub[0]:
                eyeqb[qb[0]] = destroy(qb[1].level).dag() * destroy(qb[1].level)
                eyequb[qub[0]] = destroy(qub[1].level).dag() * destroy(qub[1].level)

                inter = inter + (interaction_mat[qb[0],qub[0]]/2) * tensor(eyeqb)*tensor(eyequb)
                H_intlist.append(inter)

    for ind in range(0, len(H_intlist)): #adds interaction terms together and returns hamiltonian term for ZZ-interaction
        H_interaction = H_interaction + H_intlist[ind]

        ind += ind

    return H_interaction


