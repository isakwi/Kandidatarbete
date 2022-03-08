"""
Contains a class for adding a steps of an algorithm as well as a function creating 
a Hamiltonian from these steps.

(Not sure if the rest of the comment is relevant anymore, will leave it for later)
Definition of functions:
- CreateGates (Gate, target, NoOfGates, QbLevel) - > Tensored operator where gate acts on correct qubit
- TimeDependGates (tlist) - > QobjEvo of time dependant gate with correct drive interval
- AddGates ( QobjEvo ) - > Adds QobjEvos to final Hamiltonian

"""

import GateLib
from qutip import *
import numpy as np
import Qb_class as Qb

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

"""def CreateHFromSteps(step, n, L):
    # Maybe change the n and L inputs to a list of Qubit-objects, so that we can have different L
    x = [qeye(L) for x in range(n)]
    for i in range(len(step.name)):
        y = "GateLib."
        y += step.name[i]
        x[step.Tar_Con[i]] = Qobj(eval(y))
    return tensor(x)"""

def CreateHfromStep(step, Qblist):
    """ Create a list of Qobj from a step in the step_list
    Maybe add function to determine which are virtual gates and which are not? """
    H = []  # Try to make H pre defined in size!!!
    for i in range(len(step.name)):
        y = eval("GateLib." + step.name[i])
        H.append(y(Qblist, step.Tar_Con[0]))
        """if 2q gate:
                H.append(y(Qblist, step.Tar_Con))
            else:
                do what we did before"""
    return H

if __name__ == "__main__":
    Qblist = []
    Qblist.append(Qb.Qubit(2, [], [], []))
    Qblist.append(Qb.Qubit(2, [], [], []))

    steps = []
    steps.append(Add_step(["PX", "PY"], [0, 1], [5, 5]))
    hej = CreateHfromStep(steps[0], Qblist)
    print(hej)

"""
Ex of usage:

steps = []
steps.append(Add_step(name=["PX", "PX"], Tar_Con = [0,1], angle = [np.pi, 0]))

H = CreateHFromSteps(steps[0],2,2)

"""

"(Not sure if ths is relevant anymore)"

"For future reference, Add Gates could probably be written on this sort of form"
# H = H_anh
# for i in len(gate):
#     H= H + QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)


