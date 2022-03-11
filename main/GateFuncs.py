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

def CreateHfromStep(step, Qblist):
    """ Create two lists of Qobj from a step in the step_list, one for virtual and one for real gates
    Also return a tlist depending on what gates there are in the step """
    H_real = []  # Try to make H pre defined in size!!! 
    # Might be hard to do since we don't know how many gates will be real
    H_virt = []
    tmax = 20e-9 # Defaults to time for single qubit gate
    for i in range(len(step.name)):
        try: 
            y = eval("GateLib." + step.name[i]) # Calls the gate corresponding to the step.name[i]
        except Exception as error:
            print('A gate you are trying to perform cannot be executed. \
            \nQNAS only handles gates avaliable at Chalmers quantum computer')
            raise 
            sys.exit(1) # Stops the program
        """The error handling is probably not very good. I know one should be more specific in which errors
        to handle in each except, but all the errors in the try block must come from step.name[i] (given that
        the code works as it should), so this should be pretty safe.         
        """
        if step.name[i] in ["VPZ"]:  # Check virtual gates
            H_virt.append(y(Qblist, step.Tar_Con[i], step.angle[i]))
        elif step.name[i] in ["2qubitgates"]:  # Check 2q gates
            H_real.append(y(Qblist, step.Tar_Con[i]))
            tmax = 200e-9 # If there is a 2qb gate the maximal time changes to match that
        elif step.name[i] in ["HD"]:
            step.angle[i] = np.pi/2
            H = GateLib.HD(Qblist, step.Tar_Con[i])
            H_real.append(H[0])
            H_virt.append(H[1])
        else:  # Else append as 1q gate
            H_real.append(y(Qblist, step.Tar_Con[i]))
    return [H_real, H_virt, tmax] 


def TimeDepend(step, gates, t_max):
    angles = step.angle  # [ang1, ang2, ang3...]
    # Create tlist

    # Find theoretical max drive time ~ π rotation
    """t_max = 20 * 1e-9  # One qb gate time  MAYBE HAVE THIS AS AN INPUT?
    for Tar_Con in step.Tar_Con:
        if type(Tar_Con) == list:
            t_max = 200*1e-9   #Two qb gate time
            tlist = np.linspace(0, t_max, 100)  #Maybe make resolution an input ? 100 default
            break"""
    # Find max drive time for 1qb gates ~ largest drive angle
    if t_max < 100*1e-9:   # Python makes t_max not quite 200ns for 2qb.
        t_dmax = t_max * abs(max(angles)) / np.pi  # Drive time for the largest angle in step
        tlist = np.linspace(0, t_dmax, 100) #Maybe make resolution an input ? 100 default
    else:
        tlist = np.linspace(0,t_max,100)

    args=np.zeros(3)
    #Create time dep H from angles
    H = 0
    for i in range(len(gates)):
        gate = gates[i]
        args[0] = angles[i]  # Drive angle
        args[1] = t_max  # Theoretical max gate time (~ ang=π)
        args[2] = 0   # Start time for drive
        H = H + QobjEvo([[gate, TimeFunc(tlist, args)]], tlist=tlist)
    return [H, tlist]

if __name__ == "__main__":
    Qblist = []
    Qblist.append(Qb.Qubit(2, [], [], []))
    Qblist.append(Qb.Qubit(2, [], [], []))

    steps = []
    steps.append(Add_step(["Fake Gate", "PY", "VPZ"], [0, 1, 1], [5, 5, 5]))
    hej_real, hej_virt, tlist = CreateHfromStep(steps[0], Qblist)
    #print(hej_real)
    print(tlist)
"""
Ex of usage:

steps = []
steps.append(Add_step(name=["PX", "PX"], Tar_Con = [0,1], angle = [np.pi, 0]))

H = CreateHFromSteps(steps[0],2,2)

"""