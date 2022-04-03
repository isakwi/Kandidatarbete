
import numpy as np
import GateFuncs as gf
import CollapseOperator_function as colf
import main_Algorithm as ma
from qutip import *
import GateLib as gl
import time
import matplotlib.pyplot as plt
import Qb_class as qbc
import matplotlib as mpl
pi = np.pi
tstart=time.time()
c = 0.01

# qubits
qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])

gamma_resolution = 10
beta_resolution = 10

# list of angles for parameters
gamma_vec = np.linspace(0, pi, gamma_resolution)
beta_vec = np.linspace(0, pi, beta_resolution)
qblist = [qb1, qb2]

# zeros matrix for saving expectation value of hamiltonian
exp_mat = np.zeros((beta_resolution, gamma_resolution))
c_ops = colf.create_c_ops(qblist)
# number of trajectories
ntraj = 10
tmax= [50e-9, 271e-9]
t_st = 0
psi0 = qbc.create_psi0(qblist, 0)  # 0 is the groundstate
problem = 'a'

if problem == 'a':
    J, h1, h2 = 1/2, -1/2, 0
elif problem == 'b':
    J, h1, h2 = 0, -1, 0
elif problem == 'c':
    J, h1, h2 = 0, -1/2, -1/2
elif problem == 'd':
    J, h1, h2 = 1, 0, 0
else:
    raise ValueError("You must do problem \'a\', \'b\', \'c\' or \'d\'")
"""
INPUTS: 
    Choose Number of qubits (up to 8)
    Choose drive angle and drive start for each qubit

"""
ham = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)  # Maybe plus/minus
# steps in algoritm (the ones that change will be updated for each step)
steps = [gf.Add_step(["PX"],[0],[0.1]) for i in range(7)]  # zero angle rotation, will all be replaced

steps[0] = (gf.Add_step(["PX", "PX"], [0, 1], [pi/2, pi/2]))  # First we apply Hadamard to both qubits
steps[1] = (gf.Add_step(["PX"], [ 1], [pi/2]))  # Then we apply Hadamard to the second qubit
steps[2] = (gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps[4] = (gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps[5] = (gf.Add_step(["PY"], [1], [pi/2]))

# iterating through list of angles and saving expectation values in matrix
t00 = time.time()
t0 = time.time()
for i in range(0, gamma_resolution):
    gamma = gamma_vec[i]
    if i > 0:
        t = time.time()
        print("Time elapsed: %.2f seconds." %(t-t00))
        print("Estimated time left: %.2f seconds. \n" %((gamma_resolution-i) * (t-t0)))  # Change here
        t0 = t
    for j in range(0, beta_resolution):
        beta = beta_vec[j]
        steps[3] = (gf.Add_step(["PX"], [1], [2 * gamma * J]))
        steps[6] = (gf.Add_step(["PX", "PX"], [0, 1], [2 * beta, 2 * beta]))
# calling main_algorithm
        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": qblist, "t_max": tmax, "ntraj" : ntraj, "t_st": t_st}
        state = ma.main_algorithm(args)
# saving mean value of expectation value in matrix
        exp_mat[j, i] = np.mean(expect(ham, state))  # Beta y-axis and gamma x-axis

# plotting matrix
# plt.matshow(exp_mat, cmap = plt.get_cmap('PiYG'))  # We need to flip the matrix of we use the matshow
# Do this by putting exp_mat[beta_resolution-1-j, i] = np.mean(expect(ham, state)) in for loops!) !


fig, ax = plt.subplots()
cs = ax.contourf(gamma_vec, beta_vec, exp_mat, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
# This one plots the matrix with angles
cbar = fig.colorbar(cs, ticks=np.linspace(-1,1,9))
ax.set_title(f'Cost function F($\gamma$, \u03B2) for problem {problem}')
ax.set_xlabel("$\gamma_1$")
ax.set_ylabel("\u03B2$_1$")
labels = ["0", "$\pi$/2", "$\pi$"]
plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
plt.show()


# Find minima manually, will be fast for small matrices, like in the benchmark!
# Only finds one minimum though, not if there are many
minima = exp_mat[0][0]
coord = [0, 0]
for i in range(len(beta_vec)):
    for j in range(len(gamma_vec)):
        if exp_mat[i][j] < minima:
            minima = exp_mat[i][j]
            coord = [i, j]
print(f"Minimum value is {minima} and matrix indices [{coord[0]}, {coord[1]}]")
print(f"It is located at gamma = {gamma_vec[coord[1]]} and beta at {beta_vec[coord[0]]}")



"""
This is meant to be a file to easily implement the benchmark. I don't know if this is how 
we want to do it, but then we can just remove the file // Albin

I added one step (p = 1) of the gates as they are defined in the paper (PHYS. REV. APPLIED 14, 034010 (2020))
I am unsure of how we define the angle for the Hadamard, I wrote 0 for now // Axel
"""
print("\nDone")
print("Time elapsed: %.2f seconds." %(time.time()-tstart))