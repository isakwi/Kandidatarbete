import numpy as np
import GateFuncs as gf
import CollapseOperator_function as colf
import main_Algorithm as ma
import main as m
from qutip import *
import GateLib as gl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import Qb_class as qbc


qb1 = qbc.Qubit(3, [0.01,0.01,0.01], 0.1, [1,1], [1,0,0])
qb2 = qbc.Qubit(3, [0.01,0.01,0.01], 0.1, [2,2], [1,0,0])

gamma_vec = np.linspace(0, np.pi,20)
qblist= [qb1, qb2]

statelist= []
exp_mat = np.zeros(20,20)

c_ops = colf.create_c_ops(qblist)
ntraj = 1
tmax= [20, 200]
psi0 = m.create_psi0(qblist)
J = 0.5
h1, h2 = -0.5 , 0

ham = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)

for i in range(0, 20):
    cangle = gamma_vec[i]
    for j in range(0,20):
        bangle = gamma_vec[j]

        steps = []
        # First we apply Hadamard to both qubits
        steps.append(gf.Add_step(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.Add_step(["HD"], [1], [0]))
        steps.append(gf.Add_step(["CZnew"], [[1, 0]]))
        steps.append(gf.Add_step(["PX"], [1], [2 * cangle * J]))
        steps.append(gf.Add_step(["CZnew"], [[1, 0]]))
        steps.append(gf.Add_step(["HD"], [1], [0]))
        steps.append(gf.Add_step(["PZ", "PZ"], [0, 1], [2 * cangle * h1, 2 * cangle * h2]))
        steps.append(gf.Add_step(["PX", "PX"], [0, 1], [2 * bangle, 2 * bangle]))

        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "qblist": qblist, "tmax": tmax, "ntraj" : ntraj}

        state = ma.main_algorithm(args)


        exp_mat[i,j] = np.mean(expect(state))


plt.matshow(exp_mat)
plt.colorbar()
plt.show()


"""
gamma = [1,1]
cangle = gamma[0] #cangle = gamma (thought the name was suitable since it comes with \hat{C}
bangle = gamma[1] #cangle = beta (thought the name was suitable since it comes with \hat{B}
J = 0.5
h1, h2 = -0.5 , 0

steps = []
#First we apply Hadamard to both qubits
steps.append(gf.Add_step(["HD","HD"], [0,1], [0,0]))
steps.append(gf.Add_step(["HD"], [1], [0]))
steps.append(gf.Add_step(["CZnew"], [[1,0]]))
steps.append(gf.Add_step(["PX"], [1], [2*cangle*J]))
steps.append(gf.Add_step(["CZnew"], [[1,0]]))
steps.append(gf.Add_step(["HD"], [1], [0]))
steps.append(gf.Add_step(["PZ","PZ"], [0,1], [2*cangle*h1, 2*cangle*h2]))
steps.append(gf.Add_step(["PX","PX"], [0,1], [2*bangle, 2*bangle]))
"""


"""
This is meant to be a file to easily implement the benchmark. I don't know if this is how 
we want to do it, but then we can just remove the file // Albin

I added one step (p = 1) of the gates as they are defined in the paper (PHYS. REV. APPLIED 14, 034010 (2020))
I am unsure of how we define the angle for the Hadamard, I wrote 0 for now // Axel
"""
