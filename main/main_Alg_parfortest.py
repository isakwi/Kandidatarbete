from qutip import *
import numpy as np
import GateFuncs as gf
import mcsolving
from Anharmonicity import anharmonicity

def main_algorithm(args):
    steps = args["steps"]
    c_ops = args["c_ops"]
    init_state = args["psi0"]
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    StoreTimeDynamics = args["StoreTimeDynamics"]
    tlist_tot = [0]
    e_ops = args["e_ops"]
    expectvals = 0 # Write over this later

    psi0 = []
    for i in range(ntraj):
        psi0.append(init_state)

    H0 = anharmonicity(Qblist) # + ZZ_Interaction(Qblist)
    if c_ops != []:
        for i in range(0,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if StoreTimeDynamics:
                if steps[i].name[0] in ["VPZ"]:  # Check if VPZ step, then no time added to tlist
                    tlist_shifted = []
                else:
                    tlist_shifted = tlist + tlist_tot[-1] # Shifting the tlist to start where previous starts.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted )) # Create tlist for the entire process
            if max(tlist) >= 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops)
            for vgate in virtualgates:
                psi0= parfor(mcsolving.virtgate, psi0, vgate=vgate)
    else:
        for i in range(0,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if StoreTimeDynamics:
                if steps[i].name[0] in ["VPZ"]:  # Check if VPZ step, then no time added to tlist
                    tlist_shifted = []
                else:
                    tlist_shifted = tlist + tlist_tot[-1] # Shifting the tlist to start where previous starts.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted )) # Create tlist for the entire process
            if max(tlist) > 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=[])
            for vgate in virtualgates:
                psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
    if StoreTimeDynamics:
        tlist_tot = np.delete(tlist_tot, 0) # We get double zero in the beginning from tlist_tot = [0] initially
        return psi0, expectvals, tlist_tot
    else:
        return psi0
    
