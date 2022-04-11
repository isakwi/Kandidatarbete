##This program takes as input:
# *steps which includes t_list(s) and gates 
# *c_ops
# *anharmonicity
# * psi0_start ? (number of qubits qubits and energy levels are the important things, all qubits are assumed to be in ground state)
# * envelope fcn
##This program calls a function which performs the #gate algorithm"
##THis program should return the final state
from qutip import *
import numpy as np
import GateFuncs as gf
import mcsolving
from Anharmonicity import anharmonicity

def main_algorithm(args):
    """ The main algorithm.
    Takes in args:
    steps of the algorithm containing information
    about gates, collapes operators, initial state, list of Qubit objects and
    anharmonicity strength (and maybe ntraj?).
    What it does:
    It first converts the first step of the
    algorithm steps to a Hamiltonian, with anharmonicity. Then runs the first mcsolve
    with 'ntraj' trajectories. This returns an array (converted to list) of final states.
    It then goes to a parfor loop over the remaining steps which runs mcsolve with 1
    trajectory for each of these final states. This is done to be able to apply
    virtual gates after every step of the algorithm, and to be able to continue
    each trajectory where it left off in the last step without risking errors that
    could come from taking average states and so on
    What it returns:
    The function returns a list (of length ntraj) of the final states"""
    steps = args["steps"]
    c_ops = args["c_ops"]
    psi0 = args["psi0"]
    Qblist = args["Qblist"]
    t_max = args["t_max"]
    ntraj = args["ntraj"]
    e_ops = []
    StoreTimeDynamics = args["StoreTimeDynamics"]


    H0 = anharmonicity(Qblist) # + ZZ_Interaction(Qblist)
    ## Do first iteration for ntraj trajectories to split the mcsolve
    physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[0], Qblist, t_max)  # gates contains physical gates, virtual gates, t_max, IN THAT ORDER
    Htd, tlist = gf.TimeDepend(steps[0], physicalgates, tmax, Qblist)
    H = Htd + H0
    numberOfPhysicalSteps = len(steps)


    if StoreTimeDynamics:
        allStates = np.array([]) #a list where all states are saved
        expectop = args["expectop"]   # Assume this is a Qobj operator that can act on psi0
        if steps[0].name[0] in ["VPZ"]:  #Check if VPZ step, then no time added to tlist
            numberOfPhysicalSteps -= 1
            tlist_tot = []
        else:
            tlist_tot = tlist # Create tlist for the entire process
    if max(tlist) >= 1e-11:  # If the tlist is too small we get integration error
        if c_ops != []:
            output = mcsolve(H, psi0, tlist, c_ops=c_ops, e_ops=e_ops, ntraj=ntraj, progress_bar=None)
            psi0 = output.states[:, -1].tolist()#this is the final states
            if StoreTimeDynamics:
                allStates = np.append(allStates, (np.transpose(output.states))) #we append a list of size (ntraj x t_res) = n_traj x 10
        else:
            output = sesolve(H, psi0, tlist, e_ops=e_ops)
            psi0 = [Qobj(output.states[-1])] #If all noise rates=0, we use sesolve instead of mcsolve => only one state
            if StoreTimeDynamics:
                np.append(allStates, (np.transpose(output.states))) #we append a list of size (ntraj x t_res) = n_traj x 10
    for vgate in virtualgates:
        if not StoreTimeDynamics:
            psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
        else:
            allStates[-ntraj:] = parfor(mcsolving.virtgate, psi0, vgate = vgate) #we replace the
            #...last element with this one, since no time passes
            psi0 = allStates[-ntraj:]


    ''' I don't know if we want to have the possibility to run with no noise.. but now we do.. 
    just remove the if statements if we want to remove. Maybe it slows it down, it's before the loops so its probably ok
    '''
    if c_ops != []:
        for i in range(1,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if StoreTimeDynamics:
                if steps[i].name[0] in ["VPZ"]:  # Check if VPZ step, then no time added to tlist
                    tlist_shifted = []
                    numberOfPhysicalSteps -= 1
                else:
                    tlist_shifted = tlist + tlist_tot[-1] # Shifting the tlist to start where previous starts.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted )) # Create tlist for the entire process
            if max(tlist) >= 1e-11:
                if not StoreTimeDynamics:
                    psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops)
                else:
                    allStates= np.append(allStates, np.transpose(parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops, returnFullList = True)))
                    psi0 = allStates[-ntraj:]
            for vgate in virtualgates:
                if not StoreTimeDynamics:
                    psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)
                else:
                    allStates[-ntraj:] = (parfor(mcsolving.virtgate, psi0, vgate=vgate))  # the we replace the
                    # ...last element with this one, since no time passes
                    psi0 = allStates[-ntraj:]
    else:
        for i in range(1,len(steps)): #each step except the first one
            physicalgates, virtualgates, tmax = gf.CreateHfromStep(steps[i], Qblist, t_max)  # gates contains "physical gates", virtual gates, t_list, IN THAT ORDER
            Htd, tlist = gf.TimeDepend(steps[i], physicalgates, tmax, Qblist)
            H = Htd + H0
            if StoreTimeDynamics:
                if steps[i].name[0] in ["VPZ"]:  # Check if VPZ step, then no time added to tlist
                    tlist_shifted = []
                    numberOfPhysicalSteps -= 1
                else:
                    tlist_shifted = tlist + tlist_tot[-1]  # Shifting the tlist to start where previous starts.
                tlist_tot = np.concatenate((tlist_tot, tlist_shifted)) # Create tlist for the entire process
                if max(tlist) > 1e-11:
                    allStates[-ntraj:] = np.transpose(parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops, returnFullList = True))
                    psi0 = allStates[-ntraj:]
                for vgate in virtualgates:
                    allStates[-ntraj:] = np.transpose(parfor(mcsolving.virtgate, psi0, vgate=vgate) ) # the we replace the
                    # ...last element with this one, since no time passes
                    psi0 = allStates[-ntraj:]
            else:
                if max(tlist) > 1e-11:
                    psi0 = parfor(mcsolving.mcs, psi0, H=H, tlist=tlist, c_ops=c_ops, e_ops=e_ops)
                for vgate in virtualgates:
                    psi0 = parfor(mcsolving.virtgate, psi0, vgate=vgate)


    if StoreTimeDynamics:
        """psi0 is a 1-dim numpy array of the final states (Qobj) with length ntraj
        tlist_tot is a 1-dim numpy array of every time step in the simulation
        expectedvals is an 1-dim numpy array with the expected value of chosen operator at each time step
        allstates will be returned as a numpy array with dimensions (len(tlist_tot),ntraj), """
        allStates = np.reshape(allStates, ((numberOfPhysicalSteps)*10,ntraj))
        expectvals = np.array([np.mean(expect(expectop, parallelStates)) for parallelStates in allStates])
        return psi0,allStates, expectvals, tlist_tot #psi0 are the final state (there are ntraj of them)
    else:
        return psi0
    
