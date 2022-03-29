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
    #Hmm.. *(-1) to get positive rotations.. but to make HD correct this def^ (KDs) is correct /Ed
    #Guess we will have to ask KD about it
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
    #sz[target] = destroy(Qblist[target].level)*create(Qblist[target].level) - create(Qblist[target].level)*destroy(Qblist[target].level)
    sz[target] = create(Qblist[target].level) * destroy(Qblist[target].level)

    #If we intend this to rotate around z-axis it should be defined differently.. but I guess we us VPZ for that?
    #Yes probably
    #But we need it to work for expectation values!!
    #Made some wack ass solution by multiplying by -2 but not sure if this is legal
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
    HD_real = PY(Qblist, target)
    HD_virt = VPZ(Qblist, target, np.pi)
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

def CZ_old(Qblist, Tar_Con):#DO NOT USE THIS
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

def CZ(Qblist, Tar_Con): #DO NOT USE THIS
    """Create a controlled-Z gate, for up to 4-level qubits
    It depends only on the lowest two states though"""
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

def CZnew(Qblist, Tar_Con):
    """
    H = |11><02|+|02><11| or |11><20|+|20><11|
    so only for 3level right?"""
    k11 = tensor(basis(3, 1), basis(3, 1))
    k02 = tensor(basis(3, 2), basis(3, 0))
    H = k11 * k02.dag() + k02 * k11.dag()
    # We must add diagonal ones in order to treat all possible states (right???)
    size = H.shape[0]  # H can be represented as an size x size matrix
    H2 = np.zeros([size, size])
    for i in range(size):
        H2[i,i] = np.array_equal(H[i], H[i] * 0) # if this row is all zero, we have to put a 1 at position (i,i) to "do nothing"
        # What does this do? np.array.equal() returns true or false? Yes, which python interprets as 1 or 0
    H2 = Qobj(H2, dims = H.dims)
    #H = (H + H2)
    cz = [qeye(Qb.level) for Qb in Qblist]
    target = Tar_Con[0]  # index of the targeted qubit
    control = Tar_Con[1]  # index of the controlling qubit
    del(cz[max(Tar_Con)])  # Make room for the cz gate
    del(cz[min(Tar_Con)])  # Make room for the cz gate
    return gate_expand_2toN(H,len(Qblist),cz,control,target) # Found this function on qutip web and modified it a bit

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

def iSWAP(Qblist, Tar_Con):
    """
    Since this is a symmetric swap, both qubits are targets and controls
    To avoid enumeration of the tar/con qubits, they are still called "target" and "control"
    Takes help from the gate_expand_2toN function
    Quantum object representing the iSWAP gate.
    Returns
    -------
    iSWAP_gate : qobj
        Quantum object representation of iSWAP gate
    """
    target = Tar_Con[0]  # index of the targeted qubit
    control = Tar_Con[1]  # index of the controlling qubit
    tarLevel = Qblist[target].level
    conLevel = Qblist[control].level
    k01 = tensor(basis(conLevel, 0), basis(tarLevel, 1))
    k10 = tensor(basis(conLevel, 1), basis(tarLevel, 0))
    H = 1j * (k01 * k10.dag() + k10 * k01.dag())
    #We must add diagonal ones in order to treat all possible states (right???)
    size = H.shape[0] #H can be represented as an size x size matrix
    H2 = np.zeros([size, size])
    for i in range(size):
        H2[i,i] = np.array_equal(H[i],H[i] * 0) #if this row is all zero, we have to put a 1 at position (i,i) to "do nothing"
    H2 = Qobj(H2, dims = H.dims)
    #H = H + H2
    iSWAP = [qeye(Qb.level) for Qb in Qblist]
    del (iSWAP[max(Tar_Con)])  # Make room for the iSWAP gate
    del (iSWAP[min(Tar_Con)])  # Make room for the iSWAP gate
    return gate_expand_2toN(H, len(Qblist), iSWAP, control, target)



def gate_expand_2toN(U, N, cz, control=None, target=None, targets=None):
    #FOUND THIS AT QUTIP! Noice
    """
    Create a Qobj representing a two-qubit gate that act on a system with N
    qubits.
    Parameters
    ----------
    U : Qobj
        The two-qubit gate
    N : integer
        The number of qubits in the target space.
    control : integer
        The index of the control qubit.
    target : integer
        The index of the target qubit.
    targets : list
        List of target qubits.
    Returns
    -------
    gate : qobj
        Quantum object representation of N-qubit gate.
    """

    if targets is not None:
        control, target = targets

    if control is None or target is None:
        raise ValueError("Specify value of control and target")

    if N < 2:
        raise ValueError("integer N must be larger or equal to 2")

    if control >= N or target >= N:
        raise ValueError("control and not target must be integer < integer N")

    if control == target:
        raise ValueError("target and not control cannot be equal")

    p = list(range(N))

    if target == 0 and control == 1:
        p[control], p[target] = p[target], p[control]

    elif target == 0:
        p[1], p[target] = p[target], p[1]
        p[1], p[control] = p[control], p[1]

    else:
        p[1], p[target] = p[target], p[1]
        p[0], p[control] = p[control], p[0]
    return tensor([U] + cz).permute(p)






if __name__ == "__main__":
    """ Troubleshooting"""

    # Test specific sigmax
    sx1 = tensor(qeye(2), sigmax(), qeye(2))
    Qblist = [Qb.Qubit(2, [], [], [],[]) for i in range(0,3)]
    sx = PX(Qblist,1)
    print(sx)
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
    # But not the same as inbuilt sigmaz()?
    sz1 = sm1.dag()*sm1
    sz = PZ(Qblist,1)
    if sz1 == sz:
        print("Specific sigz works!")
    else:
        print("Specific sigz doesn't work")
        print(sz1)
        print(sz)

    # Test iSWAP
    Qblist = [Qb.Qubit(2, [], [], [],[]) for i in range(2)] + [Qb.Qubit(2, [], [], [],[])]
    iSWAP = iSWAP(Qblist, [0,2])
    print("iSWAP: ", iSWAP)

    print(sx*iSWAP)

    # Test CZnew
    Qblist = [Qb.Qubit(3, [], [], [], []) for i in range(2)] + [Qb.Qubit(3, [], [], [], [])]
    CZnew = CZnew(Qblist, [0,1])
    q1 = tensor(basis(3,0), basis(3,2)) # the state |02>
    q2 = tensor(basis(3,1), basis(3,1)) # the state |11>
    print("CZ: ", CZnew )