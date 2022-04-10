"""I created a file to just for testing our main algorithm, especially the
time dynamics implementation.
Maybe you guys already did something similar, but I couldn't find any testing in the repository."""
import numpy as np
import GateFuncs as gf
import CollapseOperator_function as colf
import main_Algorithm as ma
#import main_Alg_parfortest as ma  #Uncomment to change to parfor from the start
from qutip import *
import GateLib as gl
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import Qb_class as qbc
import matplotlib as mpl

"Global parameters"
pi = np.pi


"""Configurations below, this should be changed and tweaked to test our program sufficiently"""
c1 = 1e5 # Relaxation/Decoherence
c2 = 1e5 # Dephasing
c3 = 0 #Thermal excitation? Yet to be implemented in CollapseOperator_function
qb1 = qbc.Qubit(3, [c1, c2, c3], -229e6 * 2 * pi, [1,1], [1,0,0]) #levels, c_parameters, anharm_freq, positional coordinates, initial state
qb2 = qbc.Qubit(3, [c1, c2, c3], -225e6 * 2 * pi, [1,2], [1,0,0])
qblist = [qb1, qb2]
psi0 = qbc.create_psi0(qblist, 0)  # 0 is the groundstate
steps = []
c_ops = colf.create_c_ops(qblist)
J, h1, h2 = 1, 0, 0
gamma = 2.356
beta = 1.178

steps.append(gf.Add_step(["HD", "HD"], [0,1], [0, 0]))  # First we apply Hadamard to both qubits
steps.append(gf.Add_step([ "HD"], [1], [0]))  # Then we apply Hadamard to the second qubit
steps.append(gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps.append(gf.Add_step(["PX"], [1], [2 * gamma * J]))
steps.append(gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps.append(gf.Add_step(["HD"], [1], [0]))
steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * gamma * h1, 2 * gamma * h2]))
steps.append(gf.Add_step(["PX", "PX"], [0, 1], [2 * beta, 2 * beta]))

e_ops = []
ntraj = 100
t_max = [50e-9, 271e-9] #max drive time in seconds

expectop = gl.PZ(qblist, 0) + gl.PZ(qblist, 1)
expectop = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)  # Maybe plus/minus
state11 = tensor((basis(3,1)),(basis(3,1)))
expectop = state11 * state11.dag()




"""We create a dictionary of arguments and add them"""
args = {}
args["Qblist"] = qblist
args["t_max"] = t_max
args["ntraj"] = ntraj
args["StoreTimeDynamics"] = True
args["e_ops"] = e_ops
args["c_ops"] = c_ops
args["steps"] = steps
args["psi0"] = psi0
args["expectop"] = expectop



"""We test our program"""
finalstates,allstates, expvals, tlist = ma.main_algorithm(args)
"""Visualize result as desired"""
print("length of state list:" , len(allstates))
print("time list: ", tlist)
plt.plot(tlist, expvals)
plt.show()