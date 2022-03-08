"""
step[], angles
gates[], CreateGates
=> Tidsberoende

"""
import numpy as np
from qutip import *
from Envelope import *


#

def TimeDepend(step, gates):
    angles = step.angle  # [ang1, ang2, ang3...]
    # Create tlist

    # Find theoretical max drive time ~ π rotation
    t_max = 20 * 1e-9  # One qb gate time  MAYBE HAVE THIS AS AN INPUT?
    for Tar_Con in step.Tar_Con:
        if type(Tar_Con) == list:
            t_max = 200*1e-9   #Two qb gate time
            tlist = np.linspace(0, t_max, 100)  #Maybe make resolution an input ? 100 default
            break
    # Find max drive time for 1qb gates ~ largest drive angle
    if 195*1e-9 < t_max < 205*1e-9:   # Python makes t_max not quite 200ns for 2qb.
        t_dmax = t_max * max(angles) / np.pi  # Drive time for the largest angle in step
        tlist = np.linspace(0, t_dmax, 100) #Maybe make resolution an input ? 100 default

    args=[]
    #Create time dep H from angles
    for i in range(len(gates)):
        gate = gates[i]
        args[0] = angles[i]  # Drive angle
        args[1] = t_max  # Theoretical max gate time (~ ang=π)
        args[2] = 0   # Start time for drive

        H = H + QobjEvo([gate[i], TimeFunc(tlist, args[i])], tlist=tlist)
    return [H, tlist]


# for i in len(gate):
#     H= H + QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)