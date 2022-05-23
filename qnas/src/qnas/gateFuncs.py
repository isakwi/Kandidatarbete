__all__ = ['AlgStep', 'createGatesFromStep', 'timeDepend']

"""
Contains: 
- Class Add_step for initialising a new step in the algorithm. 
- Function CreateHFromStep(step, Qblist) that returns a list of [H_real, H_virt, tmax], where
  H_real is the Hamiltonian (Qobj) for the real part of the step, H_virt is the Hamiltonian for the virtual
  part of the step (Qobj), and tmax is the maximal time corresponding to a rotation of π for 1qb gates and 2π for CZ.
- Function TimeDepend(step, gates, t_max) which returns [H,tlist], H being a time dependent Hamiltonian (QobjEvo)
  and tlist being a list of times over which the simulation will run.
"""

from . import gateLib
from qutip import QobjEvo
from numpy import pi, linspace, zeros
from . import qubitClass as Qb
from .envelopeFunction import *
from sys import exit
from . import AnHarm

class AlgStep:
    """
    Class for creating each step in an algorithm.
    Initialises name of gate, target qubit(s) (Tar_Con) and angle of rotation
    """
    def __init__(self, name, Tar_Con, angle):
        self.name = name
        self.Tar_Con = Tar_Con
        self.angle = angle


def createGatesFromStep(step, Qblist, t_max):
    """ Create two lists of Qobj from a step in the step_list, one for virtual and one for real gates
    Also return the max drive time depending on what gates there are in the step
    t_max[0] = max for 1qb gate (~20ns) and t_max[1] = max for 2ab gate (~200ns)
    Input:
    -step = AlgStep object
    -Qblist = list of Qubit objects
    -t_max = list of max gate times for 1 and 2qb gates
    Output: list of real gates, list of virtual gates and max time for the step"""

    anyPhysicalGate = False  # assume no physical gates until they're detected.
    H_real = []
    H_virt = []
    tmax = t_max[0]  # Defaults to time for single qubit gate
    if len(step.name) > len(Qblist):
        print('Error: More gates than qubits have been put to a single depth.')
        exit(1)  # Stops the program with an error code stating that it did not run as it should
    for i in range(len(step.name)):
        try: 
            y = eval("gateLib." + step.name[i])  # Calls the gate corresponding to the step.name[i]
        except Exception as error:
            print('Error: A gate you are trying to perform cannot be executed. \
            \nQNAS only handles gates avaliable at Chalmers quantum computer')
            raise exit(1) # Stops the program
        if type(step.Tar_Con[i]) == list and max(step.Tar_Con[i]) > len(Qblist) - 1 or type(step.Tar_Con[i]) == int and \
                step.Tar_Con[i] > len(Qblist) - 1:
            print('Error: Qubit outside of the number of qubits is being targeted by Tar_Con')
            exit(1)  # Stops the program with the same error code as above
        if step.angle[i] < 0 and not (gateLib.isVirtual(step, i) or step.name[i] in ["CZ", "HD"]):
            print("Warning! Negative angle of " + str(round((step.angle[i]/pi),3)) +'π detected,' + " will be converted to " + str(round((step.angle[i] % (2*pi))/pi,3)) + "π")
            step.angle[i]=step.angle[i] % (2*pi)
        if step.angle[i] > 2 * pi and not (gateLib.isVirtual(step, i) or step.name[i] in ["CZ", "HD"]):
            print("Warning! HUGE angle of " + str(round((step.angle[i]/pi),3)) +'π detected,' + " will be converted to " + str(round((step.angle[i] % (2*pi))/pi,3)) + "π")
            step.angle[i]=step.angle[i] % (2*pi)
        if gateLib.isVirtual(step, i):
            H_virt.append(y(Qblist, step.Tar_Con[i], step.angle[i]))
        elif gateLib.isPhysicalGate(step, i):
            anyPhysicalGate = True
            H_real.append(y(Qblist, step.Tar_Con[i]))
        elif gateLib.isTwoQubitGate(step, i):
            anyPhysicalGate = True
            H_real.append(y(Qblist, step.Tar_Con[i]))
            if step.name[i] in ["CZ"]: #this is needed atm
                step.angle[i] = 2* pi
                tmax = t_max[1]
                if Qblist[step.Tar_Con[i][0]].level < 3 or Qblist[step.Tar_Con[i][1]].level < 3:
                    print('Error: CZ can only act on >3 level qubits. Qubit ' + str(step.Tar_Con[i][0]) + " = " + str(Qblist[step.Tar_Con[i][0]].level) + ", Qubit " + str(step.Tar_Con[i][1]) + " = " + str(Qblist[step.Tar_Con[i][1]].level))
                    exit(1)  # Stops the program with the same error code as above
                elif Qblist[step.Tar_Con[i][0]].level != Qblist[step.Tar_Con[i][1]].level:
                    print('Error: Both Qubits targeted by CZ need to be the same level. Qubit ' + str(step.Tar_Con[i][0]) + " = " + str(Qblist[step.Tar_Con[i][0]].level) + ", Qubit " + str(step.Tar_Con[i][1]) + " = " + str(Qblist[step.Tar_Con[i][1]].level))
                    exit(1)  # Stops the program with the same error code as above
        elif step.name[i] in ["HD"]: # HD gate feels pretty unique so I left it as it was when I found it
            anyPhysicalGate = True
            step.angle[i] = pi/2
            H = gateLib.HD(Qblist, step.Tar_Con[i])
            H_real.append(H[0])
            H_virt.append(H[1])
        else:
            print(f"No gate added for step {step.name}")
    if not anyPhysicalGate:
        tmax = 0
    return H_real, H_virt, tmax


def timeDepend(step, gates, t_max, Qblist, storeTimeDynamics):
    """
    Translates the H_real from Qobj to QobjEvo by including the drive envelope corresponding to the
    angle specified in the step, and sums all the QobjEvos together to return the entire Hamiltonian for
    the real part of the step, as well as a time list (tlist) .
    input:
    - step = AlgStep object
    - gates = real gates from createGatesFromStep
    - t_max = max gate time for the step from createGatesFromStep
    - Oblist = list of Qubit objects
    Output: Time dependant Hamiltonian and tlist for the step
    """
    angles = step.angle
    angles = [angles[i] for i in range(len(angles)) if not gateLib.isVirtual(step,i)] # this eliminates the virtual angles
    # Find max drive time for 1qb gates ~ largest drive angle
    if t_max < 100*1e-9:  # Two qubit gates have longer drive time than 100ns
        if angles != []: # If only virtual gates no angles
            t_dmax = t_max * abs(max(angles)) / pi  # Drive time for the largest angle in step
            tlist = linspace(0, t_dmax, 10)
        else:
            tlist = linspace(0,0,10)
    else:
        if storeTimeDynamics:
            tlist = linspace(0, t_max, 100)
        else:
            tlist = linspace(0,t_max,10)
    args=zeros(3)
    #Create time dep H from angles
    tol = pi/180  # Tolerance for how small angle we can handle, when an angle is "0"
                     # Now set to be able to handle at least one degree and upwards
    H=0
    for i in range(len(step.name)):
        if step.name[i] in ['CZ']:
            for j in range(2): # Removing anharmonicity for the gates targeted by CZ
                target = step.Tar_Con[i][j]
                H = H - Qblist[target].anharm/2 * AnHarm(Qblist, target)
    for i in range(len(gates)):
        if abs(angles[i]) >= tol:  # Can't add gates which have a too small angle
            gate = gates[i]
            args[0] = angles[i]  # Drive angle
            args[1] = t_max  # Theoretical max gate time (~ ang=π)
            args[2] = 0   # Start time for drive
            H = H + QobjEvo([[gate, timeFunc(tlist, args)]], tlist=tlist)
    return H, tlist

if __name__ == "__main__":
    Qblist = []
    Qblist.append(Qb.Qubit(2, [], [], []))
    Qblist.append(Qb.Qubit(2, [], [], []))
    Qblist.append(Qb.Qubit(3, [], [], []))
    Qblist.append(Qb.Qubit(3, [], [], []))

    steps = []
    steps.append(AlgStep(["iswap", "PY", "VPZ"], [[0, 1], 1, 1], [0, pi, pi]))
    hej_real, hej_virt, tlist = createGatesFromStep(steps[0], Qblist, t_max= [20e-9, 20e-9, 20e-9])
    print(hej_real)
    print(tlist)
"""
Ex of usage:

steps = []
steps.append(Add_step(name=["PX", "PX"], Tar_Con = [0,1], angle = [np.pi, 0]))

H = CreateHFromSteps(steps[0],2,2)

"""