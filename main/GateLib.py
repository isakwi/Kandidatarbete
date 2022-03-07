"""
Backend with definition of 1qb and 2qb gates
"""

from qutip import *

def PX(Qblist, target):
    """Creates specific sigmax gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator"""

    sx = [qeye(Qb.level) for Qb in Qblist]
    sx[target] = destroy(Qblist[target].level) + create(Qblist[target].level)
    return tensor(sx)

def PY(Qblist, target):
    """Creates specific sigmay gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator"""
    sy = [qeye(Qb.level) for Qb in Qblist]
    sy[target] = -1j * (destroy(Qblist[target].level) - create(Qblist[target].level))
    return tensor(sy)

def PM(Qblist, target):
    """Creates specific sigma- gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator"""
    sm = [qeye(Qb.level) for Qb in Qblist]
    sm[target] = destroy(Qblist[target].level)
    return tensor(sm)

def PZ(Qblist, target):
    """Creates specific sigmaz gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator
    This might need to be changed to be a "virtual" gate """
    sz = [qeye(Qb.level) for Qb in Qblist]
    sz[target] = create(Qblist[target].level)*destroy(Qblist[target].level)
    return tensor(sz)



