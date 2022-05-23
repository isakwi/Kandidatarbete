__all__ = ['PX', 'PY', 'PZ', 'PM', 'PP', 'VPZ', 'RPY', 'ID', 'HD',
           'CZ', 'iSWAP', 'gate_expand_2toN', 'isVirtual', 'isPhysicalGate',
           'isTwoQubitGate']

"""
Backend with definition of 1qb and 2qb gates
"""

from . import qubitClass as Qb
from qutip import qeye, create, destroy, tensor, Qobj, basis, sigmax, sigmay
from numpy import pi, exp

def ID(Qblist, target=None):
    """Creates identity gate which can be used when creating a openQASM file to make
    sure all gates are in the correct depth"""
    id = [qeye(Qb.level) for Qb in Qblist]
    return tensor(id)

def PX(Qblist, target):
    """Creates specific sigmax gate.
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    sx = [qeye(Qb.level) for Qb in Qblist]
    sx[target] = destroy(Qblist[target].level) + create(Qblist[target].level)
    return tensor(sx)

def PY(Qblist, target):
    """Creates specific sigmay gate.
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    sy = [qeye(Qb.level) for Qb in Qblist]
    sy[target] = -1j * (destroy(Qblist[target].level) - create(Qblist[target].level))
    return tensor(sy)

def RPY(Qblist, target):
    """REVERSED SIGMAY, TO BE USED IN HADAMARD
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    rsy = [qeye(Qb.level) for Qb in Qblist]
    rsy[target] = 1j* (destroy(Qblist[target].level) - create(Qblist[target].level))
    # OBS: In HD we use -PY for negative rotation.
    return tensor(rsy)

def PM(Qblist, target):
    """Creates specific sigma- gate
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    sm = [qeye(Qb.level) for Qb in Qblist]
    sm[target] = destroy(Qblist[target].level)
    return tensor(sm)

def PP(Qblist, target):
    """Creates specific sigma+ gate
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    sp = [qeye(Qb.level) for Qb in Qblist]
    sp[target] = create(Qblist[target].level)
    return tensor(sm)

def PZ(Qblist, target):
    """Creates specific sigmaz gate
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    sz = [qeye(Qb.level) for Qb in Qblist]
    sz[target] = 2 * create(Qblist[target].level) * destroy(Qblist[target].level) - qeye(Qblist[target].level)
    return tensor(sz)

def VPZ(Qblist, target, angle):
    """Creates virtual sigmaz gate,
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    - angle = angle which to virtually rotate around z-axis
    Output: Qobj that operates on qubit[target] with correct dimensions and angle"""
    vsz = [qeye(Qb.level) for Qb in Qblist]
    try:
        if Qblist[target].level == 2:
            vsz[target] = Qobj([[exp(-1j*angle/2), 0], [0, exp(1j*angle/2)]])
        elif Qblist[target].level == 3:
            vsz[target] = Qobj([[exp(-1j * angle / 2), 0, 0], [0, exp(1j * angle / 2), 0], [0, 0, 1]])
        elif Qblist[target].level == 4:
            vsz[target] = Qobj([[exp(-1j * angle / 2), 0, 0, 0], [0, exp(1j * angle / 2), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    except:
        print("Couldn't create Virtual Pauli Z gate! Maybe you dont have qubit level between 2 and 4?")
        print("Calculates the virtual pauli z gate as identity matrix!")
    return tensor(vsz)


def HD(Qblist, target):
    """Create Hadamard gate
    NOTE: Angle for HD_real is always pi/2 and for HD_virt always pi
    Input:
    - Qblist = list of Qubit objects
    - target = qubit to be targeted by the operator
    Output: Qobj that operates on qubit[target] with correct dimensions"""
    HD_real = RPY(Qblist, target)  # OBS negative PY rotation, that's why we call RPY
    HD_virt = VPZ(Qblist, target, pi)
    return [HD_real, HD_virt]

def CZ(Qblist, Tar_Con):
    """Create specific CZ gate, modelled as H = |11><02|+|02><11| or |11><20|+|20><11|
    NOTE: Only works for 3level qubits.
    Input:
    - Qblist = list of Qubit objects
    - Tar_Con = qubits to be targeted by the operator
    Output: Qobj that operates on the targeted qubits with correct dimensions"""
    k11 = tensor(basis(Qblist[Tar_Con[0]].level, 1), basis(Qblist[Tar_Con[1]].level, 1))
    k02 = tensor(basis(Qblist[Tar_Con[0]].level, 0), basis(Qblist[Tar_Con[1]].level, 2))
    H = k11 * k02.dag() + k02 * k11.dag()
    cz = [qeye(Qb.level) for Qb in Qblist]
    target = Tar_Con[0]  # index of the targeted qubit
    control = Tar_Con[1]  # index of the controlling qubit
    del(cz[max(Tar_Con)])  # Make room for the cz gate
    del(cz[min(Tar_Con)])  # Make room for the cz gate
    return gate_expand_2toN(H,len(Qblist),cz,control,target)

def iSWAP(Qblist, Tar_Con):
    """
    Saved this for now, might delete later.
    Since this is a symmetric swap, both qubits are targets and controls
    To avoid enumeration of the tar/con qubits, they are still called "target" and "control"
    Takes help from the gate_expand_2toN function
    Quantum object representing the iSWAP gate.
    Returns
    -------
    iSWAP_gate : qobj
        Quantum object representation of iSWAP gate

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
    return gate_expand_2toN(H, len(Qblist), iSWAP, control, target)"""
    raise Exception ("iSWAP is not implemented. See gateLib for more info")



def gate_expand_2toN(U, N, cz, control=None, target=None, targets=None):
    """Modified QuTiP function.
    Original source code: https://qutip.org/docs/latest/modules/qutip/qip/operations/gates.html"""
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

"""Classification of gates"""
def isVirtual(gate, i):
    if gate.name[i] in ['VPZ']:
        return True
    else:
        return False

def isTwoQubitGate(gate, i):
    if gate.name[i] in ['CZ', 'iSWAP','CZ']:
        return True
    else:
        return False

def isPhysicalGate(gate,i):
    if gate.name[i] in ['PX', 'PY', 'PZ', 'PM', 'PP', 'ID']:
        return True
    else:
        return False

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

    # Test CZ
    Qblist = [Qb.Qubit(3, [], [], [], []) for i in range(2)] + [Qb.Qubit(3, [], [], [], [])]
    CZnew = CZ(Qblist, [0, 1])
    q1 = tensor(basis(3,0), basis(3,2)) # the state |02>
    q2 = tensor(basis(3,1), basis(3,1)) # the state |11>
    print("CZ: ", CZnew)
