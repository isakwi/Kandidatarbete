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

    psi0 = []
    for i in range(ntraj):
        psi0.append(init_state)

    H0 = anharmonicity(Qblist) # + ZZ_Interaction(Qblist)
    if c_ops != []:
        for i in range(0,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if max(tlist) >= 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
            for vgate in virtualgates:
                psi0= parfor(mcsolving.virtgate, psi0, vgate=vgate)
        print("(29) psi0 = " + str(psi0))
        print(type(psi0))
    else:
        for i in range(0,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if max(tlist) > 1e-11:
                psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops)
            for vgate in virtualgates:
                psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
    return psi0
    
