"""
Backend with definition of 1qb and 2qb gates
"""

import Qb_class as Qb
from qutip import *
import numpy as np
from scipy.linalg import *

def PX(Qblist, target):
    """Creates specific sigmax gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator
    Returns a Qobj that operates on qubit[target] with the gate"""
    sx = [qeye(Qb.level) for Qb in Qblist]
    sx[target] = destroy(Qblist[target].level) + create(Qblist[target].level)
    return tensor(sx)

def PY(Qblist, target):
    """Creates specific sigmay gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator
    Returns a Qobj that operates on qubit[target] with the gate"""
    sy = [qeye(Qb.level) for Qb in Qblist]
    sy[target] = 1j * (destroy(Qblist[target].level) - create(Qblist[target].level))
    return tensor(sy)

def PM(Qblist, target):
    """Creates specific sigma- gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator
    Returns a Qobj that operates on qubit[target] with the gate"""
    sm = [qeye(Qb.level) for Qb in Qblist]
    sm[target] = destroy(Qblist[target].level)
    return tensor(sm)

def PZ(Qblist, target):
    """Creates specific sigmaz gate, maybe better than to create all gates? Then
    you can use only the operators you need.
    Input is list of qubits and which qubit you want to target with the operator
    Returns a Qobj that operates on qubit[target] with the gate"""
    sz = [qeye(Qb.level) for Qb in Qblist]
    sz[target] = create(Qblist[target].level)*destroy(Qblist[target].level)
    return tensor(sz)

def AnHarm(Qblist, target):
    """Creates anharmonicty term of correct dimension
    Input is list of qubits and which qubit you want to target with the operator
    Returns Qobj anharmonicity operator for targeted qubit """
    AH = [qeye(Qb.level) for Qb in Qblist]
    AH[target] = create(Qblist[target].level)*create(Qblist[target].level)*destroy(Qblist[target].level)*destroy(Qblist[target].level)
    return tensor(AH)

def VPZ(Qblist, target, angle):
    """Creates virtual sigmaz gate, not sure if this is the way to do it though
    Returns Qobj that operates on targeted qubit with specified angle"""
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
    """Create Hadamard gate
    Returns two operations, one real and one virtual. The virtual is to be applied after the alg-step
    NOTE: Angle for HD_real is always pi/2 and for HD_virt always pi"""
    #HD = sqrtm(PY(Qblist, target)) * PZ(Qblist,target) #we don't know if sqrtm works
    HD_real = 1/np.sqrt(2) * PY(Qblist, target)
    HD_virt = 1/np.sqrt(2) * VPZ(Qblist, target, np.pi)
    return [HD_real, HD_virt]

def CNOT(Qblist, Tar_Con):
    """Create a controlled-not gate, so far only for 2-level qubits"""
    target = Tar_Con[0]
    control = Tar_Con[1]
    if Qblist[target].level != 2:
        raise Exception("Qubit level needs to be 2!")
    outerproducts = [basis(2, 0) * basis(2,0).dag(), basis(2, 1)  * basis(2,1).dag()]
    CNOT_list_0 = [qeye(Qb.level) for Qb in Qblist]
    CNOT_list_1 = [qeye(Qb.level) for Qb in Qblist]
    CNOT_list_0[control] = outerproducts[0]
    CNOT_list_1[control] = outerproducts[1]
    CNOT_list_1[target] = sigmax()
    CNOT = tensor(CNOT_list_0) + tensor(CNOT_list_1)
    return CNOT

def CZ_old(Qblist, Tar_Con):
    """Create a controlled-Z gate, so far only for 2-level qubits"""
    target = Tar_Con[0] #index of the targeted qubit
    control = Tar_Con[1] #index of the controlling qubit
    if Qblist[target].level != 2: #we will probably allow higher levels later
        raise Exception("Qubit level needs to be 2!")
    outerproducts = [basis(2, 0) * basis(2,0).dag(), basis(2, 1) * basis(2,1).dag()] #[|0><0|, |1><1|]
    #we make one list for the control = 0 case and one for the control = 1
    CZ_list_0 = [qeye(Qb.level) for Qb in Qblist] #some of these will be replaced below
    CZ_list_1 = [qeye(Qb.level) for Qb in Qblist] #some of these will be replaced below
    CZ_list_0[control] = outerproducts[0] #this is the projection onto psi_control = 0
    CZ_list_1[control] = outerproducts[1] #this is the projection onto psi_control = 1
    CZ_list_1[target] = sigmaz() #if psi_control = 1, then we will apply sz on the target
    CZ = tensor(CZ_list_0) + tensor(CZ_list_1) #we make Kronecker products and add them up
    return CZ

def CZ(Qblist, Tar_Con):
    """Create a controlled-Z gate, for up to 4-level qubits
    It depends only on the lowest to states though"""
    target = Tar_Con[0] #index of the targeted qubit
    control = Tar_Con[1] #index of the controlling qubit
    lvl = Qblist[control].level
    outerproducts = [basis(lvl, 0) * basis(lvl,0).dag(), basis(lvl, 1) * basis(lvl,1).dag()] #[|0><0|, |1><1|]
    #we make one list for the control = 0 case and one for the control = 1
    CZ_list_0 = [qeye(Qb.level) for Qb in Qblist] #some of these will be replaced below
    CZ_list_1 = [qeye(Qb.level) for Qb in Qblist] #some of these will be replaced below
    CZ_list_0[control] = outerproducts[0] #this is the projection onto psi_control = 0
    CZ_list_1[control] = outerproducts[1] #this is the projection onto psi_control = 1
    CZ_list_1[target] = create(Qblist[target].level)*destroy(Qblist[target].level) #if psi_control = 1, then we will apply sz on the target
    CZ = tensor(CZ_list_0) + tensor(CZ_list_1) #we make Kronecker products and add them up
    return CZ

def Cnot_2qb (Qblist, targetlist, controlvalue):
    Cnotvec = [qeye(Qb.level) for Qb in Qblist] * Qblist[targetlist[0]].level
    state_con =[]
    Cnot = 0



    for ind in range(0, Qblist[targetlist[0]].level):
        state_con.append(basis(Qblist[targetlist[0]].level), ind)

    for i in range(0, Qblist[targetlist[0]].level):
        Cnotvec[i][targetlist[0]] = state_con[i] * state_con[i].dag()

    Cnotvec[controlvalue][targetlist[1]] = destroy(Qblist[1].level) + destroy(Qblist[1].level)

    for ix in range(0, len(Cnotvec)):
        Cnot = Cnot + tensor(Cnotvec[ix])

    return Cnot





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
