from qutip import *
import numpy as np
import GateFuncs as gf
import mcsolving
from Anharmonicity import anharmonicity
import ExpectationValues
import ZZinteraction_function as zz
from GateLib import *

def main_algorithm(args):
    steps = args["steps"]
    c_ops = args["c_ops"]
    init_state = args["psi0"]
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    StoreTimeDynamics = args["StoreTimeDynamics"]
    tlist_tot = [0]
    e_ops_inp = args["e_ops_inp"]
    expectvals = 0 # Write over this later

    psi0 = []
    for i in range(ntraj):
        psi0.append(init_state)

    # temporary soltuion for zz interaction below
    try:
        zz_mat = args["zz_mat"]
        H0 = anharmonicity(Qblist) + zz.ZZ_interaction(Qblist, zz_mat)
    except: # if zz interactions not specified, we skip them
        H0 = anharmonicity(Qblist)

    if not StoreTimeDynamics:
        if c_ops != []:
            for i in range(0,len(steps)): #each step except the first one
                physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
                Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
                H = Htd + H0
                if max(tlist) >= 1e-11:# might be unnecessary wrt the above if statement
                    psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=[])
                for vgate in virtualgates:
                    psi0= parfor(mcsolving.virtgate, psi0, vgate=vgate)
        else:
            for i in range(0,len(steps)): #each step except the first one
                physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
                Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
                H = Htd + H0
                if max(tlist) > 1e-11:
                    psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=[])
                for vgate in virtualgates:
                    psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
        return psi0
    if StoreTimeDynamics:
        psi, expectvals, tlist_tot = ExpectationValues.main_algorithm_expectation(args)
        """OBS OBS ^ FUNKAR INTE ATM ! Behöver fixas för att beräkna expectvals!
        Ser ut att fungera nu!"""
        return psi0, expectvals, tlist_tot
    
