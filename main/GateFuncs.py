"""
Contains: 
- Class Add_step for initialising a new step in the algorithm. 
- Function CreateHFromStep(step, Qblist) that returns a list of [H_real, H_virt, tmax], where
  H_real is the Hamiltonian (Qobj) for the real part of the step, H_virt is the Hamiltonian for the virtual
  part of the step (Qobj), and tmax is the maximal time corresponding to a rotation of π for 1qb gates and 2π for CZ.
- Function TimeDepend(step, gates, t_max) which returns [H,tlist], H being a time dependent Hamiltonian (QobjEvo)
  and tlist being a list of times over which the simulation will run.
"""

import GateLib
from qutip import * # Will probably only need 
import numpy as np
import Qb_class as Qb
from Envelope import *
import sys # For terminating upon error. We will see if this is a good way to do it
import math
import Anharmonicity

class Add_step:
    """
    Class for creating each step in an algorithm.
    Initialises name of gate, target qubit(s) (Tar_Con) and angle of rotation
    """
    def __init__(self, name, Tar_Con, angle):
        self.name = name
        self.Tar_Con = Tar_Con
        self.angle = angle

"""
Function for creating a Hamiltonian from a given step in the algorithm
"""

def CreateHfromStep(step, Qblist, t_max):
    """ Create two lists of Qobj from a step in the step_list, one for virtual and one for real gates
    Also return a tlist depending on what gates there are in the step
    t_max[0] = max for 1qb gate (~20ns) and t_max[1] = max for 2ab gate (~200ns)"""
    anyPhysicalGate = False #assume we have no physical gates until the we're told the opposite
    H_real = []  # Try to make H pre defined in size!!! 
    # Might be hard to do since we don't know how many gates will be real
    H_virt = []
    tmax = t_max[0] # Defaults to time for single qubit gate
    if len(step.name) > len(Qblist):
        print('Error: More gates than qubits have been put to a single depth.')
        sys.exit(1)  # Stops the program with an error code stating that it did not run as it should
    for i in range(len(step.name)):
        try: 
            y = eval("GateLib." + step.name[i])  # Calls the gate corresponding to the step.name[i]
        except Exception as error:
            print('Error: A gate you are trying to perform cannot be executed. \
            \nQNAS only handles gates avaliable at Chalmers quantum computer')
            raise sys.exit(1) # Stops the program
        if type(step.Tar_Con[i]) == list and max(step.Tar_Con[i]) > len(Qblist) - 1 or type(step.Tar_Con[i]) == int and \
                step.Tar_Con[i] > len(Qblist) - 1:
            print('Error: Qubit outside of the number of qubits is being targeted by Tar_Con')
            sys.exit(1)  # Stops the program with the same error code as above
        if step.angle[i] < 0 and step.name[i] not in ["VPZ"]:
            print("Warning! Negative angle of " + str(round((step.angle[i]/np.pi),3)) +'π detected,' + " will be converted to " + str(round((step.angle[i] % (2*np.pi))/np.pi,3)) + "π")
            step.angle[i]=step.angle[i] % (2*np.pi)
            print(step.angle[i])
        if step.angle[i] > 2 * np.pi and step.name[i] not in ["VPZ","CZnew"]:
            print("Warning! HUGE angle of " + str(round((step.angle[i]/np.pi),3)) +'π detected,' + " will be converted to " + str(round((step.angle[i] % (2*np.pi))/np.pi,3)) + "π")
            step.angle[i]=step.angle[i] % (2*np.pi)
        if step.angle[i] >  np.pi and step.name[i] not in ["VPZ", "CZnew"]:
            print("Warning! Too big angle of " + str(round((step.angle[i]/np.pi),3)) +'π detected,' + " QNAS is still working on a solution for this")


        """The error handling is probably not very good. I know one should be more specific in which errors
        to handle in each except, but all the errors in the try block must come from step.name[i] (given that
        the code works as it should), so this should be pretty safe.    
        
        Maybe would be good to just have a negative envelope but not sure if that's legal     
        """

        if step.name[i] in ["VPZ"]:  # Check virtual gates
            H_virt.append(y(Qblist, step.Tar_Con[i], step.angle[i]))
        elif step.name[i] in ["PX", "PY", "PZ", "PM"]:
            anyPhysicalGate = True
            H_real.append(y(Qblist, step.Tar_Con[i]))
        elif step.name[i] in ["CZ", "iSWAP","CZnew"]:  # Check 2q gates
            anyPhysicalGate = True
            H_real.append(y(Qblist, step.Tar_Con[i]))
            if step.name[i] in ["CZ","CZnew"]:  # If we want to keep the possibility to drive 2qb gates at different angles..
                step.angle[i] = 2*np.pi
            tmax =t_max[1] # If there is a 2qb gate the maximal time changes to match that
        elif step.name[i] in ["HD"]:
            anyPhysicalGate = True
            step.angle[i] = np.pi/2
            H = GateLib.HD(Qblist, step.Tar_Con[i])
            H_real.append(H[0])
            H_virt.append(H[1])
        else:  # Else append as 1q gate
            print(f"No gate added")
        if not anyPhysicalGate:
            tmax = 0
    return H_real, H_virt, tmax


def TimeDepend(step, gates, t_max, Qblist):
    """
    Translates the H_real from Qobj to QobjEvo by including the drive envelope corresponding to the
    angle specified in the step, and sums all the QobjEvos together to return the entire Hamiltonian for
    the real part of the step .
    """
    angles = step.angle  # [ang1, ang2, ang3...]
    # Create tlist

    # Find max drive time for 1qb gates ~ largest drive angle
    if t_max < 100*1e-9:   #Python makes t_max not quite 200ns for 2qb, so we add a large safety margin ;).
        t_dmax = t_max * abs(max(angles)) / np.pi  # Drive time for the largest angle in step
        tlist = np.linspace(0, t_dmax, 10) #Maybe make resolution an input? Doesn't really matter.
                                        # Only specifies times where to store the states/e_ops
    else:
        tlist = np.linspace(0,t_max,10)
    args=np.zeros(3)
    #Create time dep H from angles
    tol = np.pi/180  # Tolerance for how small angle we can handle, when an angle is "0"
                     # Now set to be able to handle at least one degree and upwards
    H=0
    for i in range(len(step.name)):
        if step.name[i] in ['CZnew']:
            for j in range(2): # Removing anharmonicity for the gates targeted by CZ
                target = step.Tar_Con[i][j]
                H = H - Qblist[target].anharm*Anharmonicity.AnHarm(Qblist, target)
    for i in range(len(gates)):
        if abs(angles[i]) >= tol:  # Dont add gates which have a too small angle
            gate = gates[i]
            args[0] = angles[i]  # Drive angle
            args[1] = t_max  # Theoretical max gate time (~ ang=π)
            args[2] = 0   # Start time for drive
            H = H + QobjEvo([[gate, TimeFunc(tlist, args)]], tlist=tlist)
    return H, tlist

if __name__ == "__main__":
    Qblist = []
    Qblist.append(Qb.Qubit(2, [], [], []))
    Qblist.append(Qb.Qubit(2, [], [], []))
    Qblist.append(Qb.Qubit(3, [], [], []))
    Qblist.append(Qb.Qubit(3, [], [], []))

    steps = []
    steps.append(Add_step(["iswap", "PY", "VPZ"], [[0,1], 1, 1], [0, np.pi, np.pi]))
    hej_real, hej_virt, tlist = CreateHfromStep(steps[0], Qblist, t_max= [20e-9,20e-9,20e-9])
    print(hej_real)
    print(tlist)
"""
Ex of usage:

steps = []
steps.append(Add_step(name=["PX", "PX"], Tar_Con = [0,1], angle = [np.pi, 0]))

H = CreateHFromSteps(steps[0],2,2)

"""