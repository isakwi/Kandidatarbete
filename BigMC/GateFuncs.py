"""
Contains: 
- Class Add_step for initialising a new step in the algorithm. 
- Function CreateHFromStep(step, Qblist) that returns a list of [H_real, H_virt, tmax], where
  H_real is the Hamiltonian for the real part of the step, H_virt is the Hamiltonian for the virtual 
  part of the step, and tmax is the maximal time corresponding to a rotation of pi. 
- Function TimeDepend(step, gates, t_max) which returns [H,tlist], H being a time dependent Hamiltonian 
  and tlist being a list of times over which the simulation will run.
"""

import GateLib
from qutip import * # Will probably only need 
import numpy as np
import Qb_class as Qb
from Envelope import *
import sys # For terminating upon error. We will see if this is a good way to do it
import math

"""
Class for creating each step in an algorithm. 
Initialises name of gate, target qubit (Tar_Con) and angle of rotation
"""
class Add_step:
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
    H_real = []  # Try to make H pre defined in size!!!
    real_angles = []
    # Might be hard to do since we don't know how many gates will be real
    H_virt = []
    virt_angles = []
    tmax = t_max[0] # Defaults to time for virtual gate
    if len(step.name) > len(Qblist):
        print('Error: More gates than qubits have been put to a single depth.')
        sys.exit(1)  # Stops the program
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
            sys.exit(1)  # Stops the program
        """The error handling is probably not very good. I know one should be more specific in which errors
        to handle in each except, but all the errors in the try block must come from step.name[i] (given that
        the code works as it should), so this should be pretty safe.         
        """

        if step.name[i] in ["VPZ"]:  # Check virtual gates
            #H_virt.append(y(Qblist, step.Tar_Con[i], step.angle[i]))
            H_virt.append(GateLib.PZ(Qblist, step.Tar_Con[i]))
            virt_angles.append(step.angle[i])
        elif step.name[i] in ["PX", "PY", "PZ", "PM", "RPY"]:
            H_real.append(y(Qblist, step.Tar_Con[i]))
            real_angles.append(step.angle[i])
        elif step.name[i] in ["CZ", "iSWAP","CZnew"]:  # Check 2q gates
            H_real.append(y(Qblist, step.Tar_Con[i]))
            step.angle[i] = 2*np.pi  # Should it be 2*pi for all 2qb gatess??
            real_angles.append(step.angle[i])
            tmax =t_max[1] # If there is a 2qb gate the maximal time changes to match that
        elif step.name[i] in ["HD"]:
            tmax = tmax  # We need to first do real gate then virtual
            real_angles.append(np.pi/2)
            virt_angles.append(np.pi)
            H = GateLib.HD(Qblist, step.Tar_Con[i])
            H_real.append(H[0])
            H_virt.append(H[1])
        else:  # Else append as 1q gate
            print(f"No gate added")

        angles = real_angles + virt_angles
        if tmax < 100e-9:
            td = tmax*abs(max(angles))/np.pi
        else:
            td = tmax
    return H_real, real_angles, H_virt, virt_angles, tmax, td


def TimeDepend(step, angles, gates, td, Qblist, t_st, tlist, t_max):
    # Create tlist

    # Find theoretical max drive time ~ π rotation
    """t_max = 20 * 1e-9  # One qb gate time  MAYBE HAVE THIS AS AN INPUT?
    for Tar_Con in step.Tar_Con:
        if type(Tar_Con) == list:
            t_max = 200*1e-9   #Two qb gate time
            tlist = np.linspace(0, t_max, 100)  #Maybe make resolution an input ? 100 default
            break"""
    # Find max drive time for 1qb gates ~ largest drive angle

    args=np.zeros(3)
    args2 = np.zeros(2)
    #Create time dep H from angles
    tol = np.pi/180  # Tolerance for how small angle we can handle, when an angle is "0"
                     # Now set to be able to handle at least one degree and upwards
    H=0
    for i in range(len(step.name)):
        if step.name[i] in ['CZnew']:
            for j in range(2): # Removing anharmonicity for the gates targeted by CZ
                #OBS: Has to be time dependant in BigMC solution
                target = step.Tar_Con[i][j]
                args2[0] = t_max  # Max gate time
                args2[1] = t_st  # Start time for drive
                H = H - QobjEvo([[Qblist[target].anharm*GateLib.AnHarm(Qblist, target),TimeFunc2(tlist,args2)]],tlist=tlist)
    for i in range(len(gates)):
        if abs(angles[i]) >= tol:  # Skip gates which have a too small angle
            gate = gates[i]
            args[0] = angles[i]  # Drive angle
            args[1] = t_max  # Max gate time
            args[2] = t_st   # Start time for drive
            H = H + QobjEvo([[gate, TimeFunc(tlist, args)]], tlist=tlist)
    return H

def TimeDependVirt(step, angles, gates, td, Qblist, t_st, tlist, t_max):

    args=np.zeros(2)
    #Create time dep H from angles
    tol = np.pi/180  # Tolerance for how small angle we can handle, when an angle is "0"
                     # Now set to be able to handle at least one degree and upwards
    H=0
    for i in range(len(gates)):
        if abs(angles[i]) >= tol:  # Dont add gates which have a too small angle
            gate = gates[i]
            args[0] = 1e-9  # Max gate time, creates short but strong pulse
            args[1] = t_st + td   # Start time for drive, starts at the last step
            H = H + QobjEvo([[gate, 1e9/2*angles[i]*TimeFunc2(tlist, args)]], tlist=tlist)
    return H

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