__all__ = ['mainAlgorithm']

from . import gateFuncs as gf
from . import mcSolving
from .anharmonicity import anharmonicity
from . import storeTimeDynamicsMain
from . import zzInteractionFunction as zz
from qutip import parfor
def mainAlgorithm(args):
    """
    Main algorithm.
    parallell for loop solver for the ntraj trajectories for the entire quantum algorithm.
    Input: in form of an args dictionary
    - steps = list of AlgStep objects
    - c_ops = list of collapse operators
    - psi0 = initial state (|00000 .. >)
    - Qblist = list of Qubit objects
    - t_max = list of maximum gate times for 1 and 2qb gates
    - ntraj = number of trajectories
    - zz_mat = matrix for the ZZ interaction, optional.
    - StoreTimeDynamics = boolean for option to store the time dynamics.
            Then also input on e_ops is needed.
            - e_ops_inp = [[e_op1, Tar_Con],
                            [e_op2, Tar_Con], ... ]
                        where e_op is a Qobj with the dimensions  ( qubit.level x qubit.level )
                        and Tar_Con is the target and control in case of 2qb gate, as before.
    Output: ntraj number of final states
    or if StoreTimeDynamics = True: also list of expectation values at each time and total time list
    """
    steps = args["steps"]
    c_ops = args["c_ops"]
    init_state = args["psi0"]
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    StoreTimeDynamics = args["StoreTimeDynamics"]

    psi0 = []
    for i in range(ntraj):
        psi0.append(init_state)

    try:
        zz_mat = args["zz_mat"]
        H0 = anharmonicity(Qblist) + zz.zzInteraction(Qblist, zz_mat)
    except: # if zz interactions not specified, we skip them
        H0 = anharmonicity(Qblist)

    if not StoreTimeDynamics:
        if c_ops != []:
            for i in range(0,len(steps)):
                physicalgates, virtualgates, tmax = gf.createGatesFromStep(steps[i], Qblist, t_max)
                Htd, tlist = gf.timeDepend(steps[i], physicalgates, tmax, Qblist, storeTimeDynamics=False)
                H = Htd + H0
                if max(tlist) >= 1e-11:  # To avoid integration error
                    psi0 = parfor(mcSolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
                for vgate in virtualgates:
                    psi0= parfor(mcSolving.virtgate, psi0, vgate=vgate)
        else:
            psi0 = psi0[0]
            for i in range(0,len(steps)):
                physicalgates, virtualgates, tmax = gf.createGatesFromStep(steps[i], Qblist, t_max)
                Htd, tlist = gf.timeDepend(steps[i], physicalgates, tmax, Qblist, storeTimeDynamics=False)
                H = Htd + H0
                if max(tlist) > 1e-11: # To avoid integration error
                    psi0 = mcSolving.mcs(psi0, H=H, tlist=tlist, c_ops=c_ops)
                for vgate in virtualgates:
                    psi0 = mcSolving.virtgate( psi0, vgate=vgate)
        return psi0
    if StoreTimeDynamics:
        psi, expectvals, tlist_tot = storeTimeDynamicsMain.mainAlgorithmExpectation(args)
        return psi, expectvals, tlist_tot
    
