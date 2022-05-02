__all__ = ['envelopeFunc', 'timeFunc']

from numpy import sin, pi, heaviside


def envelopeFunc (t, beta, t_d, t_st):
    """ Models the drive pulse as E(t) = A*sin^2(t*π/t_d),
     Input: -beta = drive strength
            -t_d = drive time
            -t_st = start time (not used since we use different tlist for each step, => t_st = 0 always)
    Output: E(t) = A*sin^2(t*π/t_d)
    """
    E  = beta*sin((t-t_st)*pi/t_d)**2
    return E*heaviside(t_st+t_d-t,1)*heaviside(t-t_st,1)


def timeFunc (t, args):
    """
    Used for creating QobjEvos in the GateFuncs.TimeDepend function, which specifies the args for a given gate.
    Calculates the drive strength (beta) from the max time ~ π rotation (2π for 2qb gate) and
    the drive time as being a an angular fraction of the max time.
    Input: - Drive angle
           - Max gate time (~ ang=π 1qb gates , 2π CZ)
           - Start time for drive (always =0 in current solution)
           - t = element of tlist
    Output: Envelope function E(t)
    """
    ang  = args[0]  # Drive angle 
    t_m  = args[1]  # Max gate time (~ ang=π 1qb gates , 2π CZ)
    t_st = args[2]  # Start time for drive 
    if t_m < 100*1e-9:   # 2qb gates have longer drive time than 100ns
        beta = pi/t_m    # Drive strength corresponds to π drive angle for 1 qb gates
        t_d = t_m * ang / pi  # Drive time for specified angle
    else:
        beta = 2*pi/t_m  # Drive strength should correspond to 2π drive angle for 2qb gates
        t_d = t_m*ang/(2*pi)
    return envelopeFunc(t, beta, t_d, t_st)

