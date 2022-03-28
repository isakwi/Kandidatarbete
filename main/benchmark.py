import numpy as np
import GateFuncs as gf
import CollapseOperator_function as colf
import main_Algorithm as ma
from qutip import *
import GateLib as gl
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import Qb_class as qbc
pi = np.pi

c = 0.00

# qubits
qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])

gamma_resolution = 6
beta_resolution = 6

# list of angles for parameters
gamma_vec = np.linspace(0, pi, gamma_resolution)
beta_vec = np.linspace(0, pi, beta_resolution)
qblist = [qb1, qb2]

# zeros matrix for saving expectation value of hamiltonian
exp_mat = np.zeros((beta_resolution, gamma_resolution))
c_ops = colf.create_c_ops(qblist)
# number of trajectories
ntraj = 100
tmax= [50e-9, 271e-9]
psi0 = qbc.create_psi0(qblist)
problem = 'c'

if problem == 'a':
    J, h1, h2 = 1/2, -1/2, 0
elif problem == 'b':
    J, h1, h2 = 0, -1, 0
elif problem == 'c':
    J, h1, h2 = 0, -1/2, -1/2
elif problem == 'd':
    J, h1, h2 = 1, 0, 0

# Ising hHamiltonian, our cost function is the expectation value of this hamiltonian
ham = -h1 * gl.PZ(qblist, 0) - h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)  # Maybe plus/minus

# steps in algoritm (the ones that change will be updated for each step)
steps = [gf.Add_step("PX",[0],[0]) for i in range(8)]  # zero angle rotation, will all be replaced

steps[0] = (gf.Add_step(["HD", "HD"], [0, 1], [0, 0]))  # First we apply Hadamard to both qubits
steps[1] = (gf.Add_step(["HD"], [1], [0]))
steps[2] = (gf.Add_step(["CZnew"], [[1, 0]], [0]))
steps[4] = (gf.Add_step(["CZnew"], [[1, 0]], [0]))
steps[5] = (gf.Add_step(["HD"], [1], [0]))

# iterating through list of angles and saving expectation values in matrix
t0 = time.time()
for i in range(0, gamma_resolution):
    gamma = gamma_vec[i]
    if i > 0:
        t = time.time()
        print("Time elapsed: %.2f seconds." %(t-t0))
        print("Estimated time left: %.2f seconds. \n" %((gamma_resolution-i) * (t-t0)/i))  # Change here
    for j in range(0, beta_resolution):
        beta = beta_vec[j]
        steps[3] = (gf.Add_step(["PX"], [1], [2 * gamma * J]))
        steps[6] = (gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * gamma * h1, 2 * gamma * h2]))
        steps[7] = (gf.Add_step(["PX", "PX"], [0, 1], [2 * beta, 2 * beta]))
# calling main_algorithm
        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": qblist, "t_max": tmax, "ntraj" : ntraj}
        state = ma.main_algorithm(args)
# saving mean value of expectation value in matrix
        exp_mat[j, i] = np.mean(expect(ham, state))  # Beta y-axis and gamma x-axis

# plotting matrix
# plt.matshow(exp_mat)  # We need to flip the matrix of we use the matshow
# Do this by putting exp_mat[beta_resolution-1-j, i] = np.mean(expect(ham, state)) in for loops!) !
plt.contourf(gamma_vec, beta_vec, exp_mat)  # This one plots the matrix with angles
plt.colorbar()
plt.show()

# Find minima manually, will be fast for small matrices, like in the benchmark!
# Only finds one minimum though, not if there are many
minima = exp_mat[0][0]
coord = [0, 0]
for i in range(len(exp_mat)):
    for j in range(len(exp_mat)):
        if exp_mat[i][j] < minima:
            minima = exp_mat[i][j]
            coord = [i, j]
print(f"Minimum value is {minima} and matrix indices [{coord[0]}, {coord[1]}]")
print(f"It is located at gamma = {gamma_vec[coord[1]]} and beta at {beta_vec[coord[0]]}")

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
print("Done")