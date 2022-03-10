"""
Definition of Envelope function and Beta-calc func
- Envelope: (t_start, t_gate) - > E(t) (~cos^2(t))
- BetaCalc: (t_max) -> beta that takes transformation to exactly π
"""

import numpy as np


def EnvelopeFunc (t, beta, t_m, t_d, t_st): 
    # Models the drive pulse as E(t) = A*cos^2(tπ/t_d - π/2), 
    # Used in the time functions Et# which are used in H = QobjEvo 
    # beta = drive strength
    # t_m = t_max gate time (~ ang=π)
    # t_d =drive time, 
    # t_st = start time 
    E    = beta/2*np.sin((t-t_st)*np.pi/t_d)**2
    return E*np.heaviside(t_st+t_d-t,1)*np.heaviside(t-t_st,1)


def TimeFunc (t, args): 
    # To be called from QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)
    # where inputs[i] is an array of vals for i:th qubit
    ang  = args[0]  # Drive angle 
    t_m  = args[1]  # Max gate time (~ ang=π)
    t_st = args[2]  # Start time for drive 
    if t_m < 100*1e-9:   # Python makes t_max not quite 200ns for 2qb.
        beta = 2*np.pi/t_m    #Drive strength
    else: beta = 4*np.pi/t_m  #Drive strength should corespond to 2π drive angle for 2qb gates
    t_d = t_m * ang/np.pi # Drive time for specified angle
    return EnvelopeFunc(t, beta, t_m, t_d, t_st)

