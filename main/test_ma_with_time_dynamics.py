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
c1 = 1e-2 # Relaxation/Decoherence
c2 = 1e-2 # Dephasing
c3 = 0 #Thermal excitation? Yet to be implemented in CollapseOperator_function
qb1 = qbc.Qubit(3, [c1, c2, c3], -229e6 * 2 * pi, [1,1], [1,0,0]) #levels, c_parameters, anharm_freq, positional coordinates, initial state
qb2 = qbc.Qubit(3, [c1, c2, c3], -225e6 * 2 * pi, [1,2], [1,0,0])
qblist = [qb1, qb2]
psi0 = qbc.create_psi0(qblist, 0)  # 0 is the groundstate
steps = []
c_ops = colf.create_c_ops(qblist)
J, h1, h2 = 1, 0, 0
gamma1, gamma2 = 0.498, 0.675
beta1, beta2 = 0.386, 0.934

# {'bangle1': 0.38625749927352887, 'bangle2': 0.9338998705777307, 'cangle1': 0.4983658373499303, 'cangle2': 0.6747157321745737}}

steps.append(gf.Add_step(["HD", "HD"], [0,1], [0, 0]))  # First we apply Hadamard to both qubits
steps.append(gf.Add_step([ "HD"], [1], [0]))  # Then we apply Hadamard to the second qubit
steps.append(gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps.append(gf.Add_step(["PX"], [1], [2 * gamma1 * J]))
steps.append(gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps.append(gf.Add_step(["HD"], [1], [0]))
steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * gamma1 * h1, 2 * gamma1 * h2]))
steps.append(gf.Add_step(["PX", "PX"], [0, 1], [2 * beta1, 2 * beta1]))
steps.append(gf.Add_step([ "HD"], [1], [0]))  # Then we apply Hadamard to the second qubit
steps.append(gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps.append(gf.Add_step(["PX"], [1], [2 * gamma2 * J]))
steps.append(gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps.append(gf.Add_step(["HD"], [1], [0]))
steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * gamma2 * h1, 2 * gamma2 * h2]))
steps.append(gf.Add_step(["PX", "PX"], [0, 1], [2 * beta2, 2 * beta2]))



e_ops = []
ntraj = 10
t_max = [50e-9, 271e-9] #max drive time in seconds

#expectop = gl.PZ(qblist, 0) + gl.PZ(qblist, 1)
expectop1 = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)  # Maybe plus/minus
#state11 = tensor((basis(3,1)),(basis(3,1)))
state02 = tensor((basis(3,0)),(basis(3,2)))
state20 = tensor((basis(3,2)),(basis(3,0)))
#expectop2 = state02 * state02.dag() + state20 * state20.dag()
expectop2 = destroy(3)

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
args["e_ops_inp"] = [[expectop1, [0,1]], [expectop2, 1]]



"""We test our program"""
finalstates, expvals, tlist = ma.main_algorithm(args)
#finalstates, expvals, tlist = ma.main_algorithm(args)
"""Visualize result as desired"""
#print("time list: ", tlist)
print("final states data type:" , type(finalstates))
#print("expected values data type: " , type(expvals))
#print("tlist data type: " , type(tlist))

plt.plot(tlist, expvals[0])
plt.plot(tlist, expvals[1])
plt.show()