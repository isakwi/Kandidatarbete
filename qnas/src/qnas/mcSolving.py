__all__ = ['mcs', 'mcsTimeDynamics', 'virtgate']

from qutip import mcsolve, sesolve

def mcs(psi,H,tlist,c_ops):
    """
    Used for the parfor operations in mainAlgorithm.py.
    Inputs:
    - psi = state (qobj) which is iterated
    - H = Hamiltonian for the step
    - tlist = time list for the step
    - c_ops = collapse operators
    Output: Final state after each step
    """
    if c_ops != []:
        output = mcsolve(H, psi, tlist, c_ops=c_ops, e_ops = [], ntraj=1, progress_bar=None)
        outstate = (output.states[:, -1])
        return outstate[0]

    else:
        output = sesolve(H, psi, tlist, e_ops = [])
        outstate = output.states[-1]
        return outstate

def mcsTimeDynamics(psi, H, tlist, c_ops):
    """Use this if StoreTimeDynamics=True.
    Returns all states at each time in tlist instead of just final state"""
    if c_ops != []:
        output = mcsolve(H, psi, tlist, c_ops=c_ops, e_ops=[], ntraj=1, progress_bar=None)
        outstates = output.states
        return outstates
    else:
        output = sesolve(H, psi, tlist, e_ops=[])
        outstates = output.states
        return outstates


def virtgate(psi,vgate):
    """Applies virtual gate through matrix multiplication
    Input:
    - psi = State (Qobj ket)
    - vgate = virtual gate (Qobj matrix)
    Output: final state after virtual gate"""
    return vgate*psi