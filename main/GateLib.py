"""
Backend with definition of 1qb and 2qb gates
"""

import Qb_class as Qb
from qutip import *
import numpy as np

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

def AnHarm(Qblist, target):
    """Creates anharmonicty term of correct dimension
    Input is list of qubits and which qubit you want to target with the operator
    This might need to be changed to be a "virtual" gate """
    AH = [qeye(Qb.level) for Qb in Qblist]
    AH[target] = create(Qblist[target].level)*create(Qblist[target].level)*destroy(Qblist[target].level)*destroy(Qblist[target].level)
    return tensor(AH)

def VPZ(Qblist, target, angle):
    """Creates virtual sigmaz gate, not sure if this is the way to do it though
    Maybe change this so that it takes an array of targets and array of angles?"""
    vsz = [qeye(Qb.level) for Qb in Qblist]
    try:
        if Qblist[target].level == 2:
            vsz[target] = Qobj([[np.exp(-1j*angle/2), 0], [0, np.exp(1j*angle/2)]])
        elif Qblist[target].level == 3:
            vsz[target] = Qobj([[np.exp(-1j * angle / 2), 0, 0], [0, np.exp(1j * angle / 2), 0], [0, 0, 1]])
        elif Qblist[target].level == 4:
            vsz[target] = Qobj([[np.exp(-1j * angle / 2), 0, 0, 0], [0, np.exp(1j * angle / 2), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    except:
        print("Couldn't create Virtual Pauli Z gate! Maybe you dont have qubit level between 2 and 4?")
        print("Calculates the virtual pauli z gate as identity matrix!")
    return tensor(vsz)


def HD(Qblist, target):
    """Create Hadamard gate, angle for this gate should always be pi/2!!"""
    HD = sqrtm(PY(Qblist, target)) * PZ(Qblist,target) #we don't know if sqrtm works
    return HD


if __name__ == "__main__":
    """ Troubleshooting"""

    # Test specific sigmax
    sx1 = tensor(qeye(2), sigmax(), qeye(2))
    Qblist = [Qb.Qubit(2, [], [], []) for i in range(0,3)]
    sx = PX(Qblist,1)
    if sx1 == sx:
        print("Specific sigx works!")
    else:
        print("Specific sigx doesn't work")
        print(sx1)
        print(sx)

    # Test specific sigmay
    sy1 = tensor(qeye(2), sigmay(), qeye(2))
    sy = PY(Qblist,1)
    if sy1 == sy:
        print("Specific sigy works!")
    else:
        print("Specific sigy doesn't work")
        print(sy1)
        print(sy)

    # Test specific sigmam
    sm1 = tensor(qeye(2), destroy(2), qeye(2))
    sm = PM(Qblist, 1)
    if sy1 == sy:
        print("Specific sigm works!")
    else:
        print("Specific sigm doesn't work")
        print(sy1)
        print(sy)


    # Test specific sigmaz
    sz1 = sm1.dag()*sm1
    sz = PZ(Qblist,1)
    if sz1 == sz:
        print("Specific sigz works!")
    else:
        print("Specific sigz doesn't work")
        print(sz1)
        print(sz)

    hej = VPZ(Qblist, )

def Cnot_2qb (Qblist, targetlist):
    Cnotvec = [qeye(Qb.level) for Qb in Qblist] * Qblist[targetlist[0]].level
    state_con =[]
    Cnot = 0



    for ind in range(0, Qblist[targetlist[0]].level):
        state_con.append(basis(Qblist[targetlist[0]]), ind)

    for i in range(0, Qblist[targetlist[0]].level):
        Cnotvec[i][targetlist[0]] = state_con[i] * state_con[i].dag()
        Cnotvec[i][targetlist[1]] = destroy(Qblist[1].level) + destroy(Qblist[1].level)


    for ix in range(0, len(Cnotvec)):
        Cnot = Cnot + tensor(Cnotvec[ix])

    return Cnot




    scon0 = basis(Qblist[targetlist[0]].level, 0)
    scon1 = basis(Qblist[targetlist[0]].level, 1)







    return

