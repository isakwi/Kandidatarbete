"""
Contains the definition of the Envelope and TimeFunc functions
- EnvelopeFunc: given a the drive strength and a set of times, returns the drive pulse E(t) ~ sin^2(t)
- TimeFunc: To be called from GateFuncs.TimeDepend with the args from the specific step,
            calculates the drive strength (beta) from the drive angle
            and the drive time from the angle and maximal gate time.
"""

import numpy as np


def EnvelopeFunc (t, beta, t_d, t_st):
    """ Models the drive pulse as E(t) = A*sin^2(t*π/t_d),
     -beta = drive strength
     -t_d = drive time
     -t_st = start time (not used since we use different tlist for each step, => t_st = 0 always)
    """
    E    = beta*np.sin((t-t_st)*np.pi/t_d)**2
    return E*np.heaviside(t_st+t_d-t,1)*np.heaviside(t-t_st,1)


def TimeFunc (t, args): 
    """
    Used for creating QobjEvos in the GateFuncs.TimeDepend function, which specifies the args for a given gate.
    Calculates the drive strength (beta) from the max time ~ π rotation (2π for 2qb gate) and
    the drive time as being a an angular fraction of the max time.
    """
    ang  = args[0]  # Drive angle 
    t_m  = args[1]  # Max gate time (~ ang=π 1qb gates , 2π CZ)
    t_st = args[2]  # Start time for drive 
    if t_m < 100*1e-9:   # Python makes t_max not quite 200ns for 2qb. (#todo: Mer robust lösning här kanske...)
        beta = np.pi/t_m    #Drive strength corresponds to π drive angle for 1 qb gates
        t_d = t_m * ang / np.pi  # Drive time for specified angle
    else:
        beta = 2*np.pi/t_m  #Drive strength should corespond to 2π drive angle for 2qb gates
        t_d = t_m*ang/(2*np.pi) # ? Do we want to drive to different angles? or always 2π ?
        #todo: make solution for iSWAP where we want pi as angle, either here ore elsewhere in the program
        # ^ Should the drive strength change as well?
    return EnvelopeFunc(t, beta, t_d, t_st)

