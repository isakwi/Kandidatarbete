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
import matplotlib as mpl
pi = np.pi

c = 0.01

# qubits
qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])

betaplot = False #make this true if we want 1D plots as well

gamma_resolution = 20
beta_resolution = 20

# list of angles for parameters
gamma_vec = np.linspace(0, pi, gamma_resolution)
beta_vec = np.linspace(0, pi, beta_resolution)
qblist = [qb1, qb2]

# zeros matrix for saving expectation value of hamiltonian
exp_mat = np.zeros((beta_resolution, gamma_resolution))
if betaplot:
    state_mat = list([[qeye(1) for i in range(gamma_resolution)] for j in range(beta_resolution)])
c_ops = colf.create_c_ops(qblist)
# number of trajectories
ntraj = 100
tmax= [50e-9, 271e-9]
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

# Ising hHamiltonian, our cost function is the expectation value of this hamiltonian
ham = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)  # Maybe plus/minus

# Changed the sign of J again and then it kinda worked

# steps in algoritm (the ones that change will be updated for each step)
steps = [gf.Add_step(["PX"],[0],[0.1]) for i in range(8)]  # zero angle rotation, will all be replaced

steps[0] = (gf.Add_step(["HD", "HD"], [0, 1], [0, 0]))  # First we apply Hadamard to both qubits
steps[1] = (gf.Add_step([ "HD"], [ 1], [0]))  # Then we apply Hadamard to the second qubit
steps[2] = (gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps[4] = (gf.Add_step(["CZnew"], [[1,0]], [2*pi]))
steps[5] = (gf.Add_step(["HD"], [1], [0]))

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
        steps[6] = (gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * gamma * h1, 2 * gamma * h2]))
        steps[7] = (gf.Add_step(["PX", "PX"], [0, 1], [2 * beta, 2 * beta]))
# calling main_algorithm
        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": qblist, "t_max": tmax, "ntraj" : ntraj}
        state = ma.main_algorithm(args)
# saving mean value of expectation value in matrix
        exp_mat[j, i] = np.mean(expect(ham, state))  # Beta y-axis and gamma x-axis
        if betaplot:
            state_mat[j][i] = state[0].data

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


if betaplot:
    fig, ax2 = plt.subplots()
    cost_vec = exp_mat[coord[1]][:]
    state_vec = state_mat[coord[1]][:]
    zz = [state[0, 0] for state in state_vec]  # |00>
    zz = [np.abs(amp) ** 2 for amp in zz]
    zo = [state[1, 0] for state in state_vec]  # |01>
    zo = [np.abs(amp) ** 2 for amp in zo]
    oz = [state[3, 0] for state in state_vec]  # |10>
    oz = [np.abs(amp) ** 2 for amp in oz]
    oo = [state[4, 0] for state in state_vec]  # |11>
    oo = [np.abs(amp) ** 2 for amp in oo]
    ax2.plot(beta_vec, zz, 'yo', label="P(|00>)")
    ax2.plot(beta_vec, zo, 'ro', label="P(|01>)")
    ax2.plot(beta_vec, oz, 'go', label="P(|10>)")
    ax2.plot(beta_vec, oo, 'ko', label="P(|11>)")
    ax2.plot(beta_vec, cost_vec, 'mo', label="F")
    ax2.legend()
    ax.set_title('Problem {problem}')
    imStr = "betaplot" + str(problem) + ".pdf"
    plt.show()
    plt.savefig(imStr, format="pdf", bbox_inches="tight")

"""
This is meant to be a file to easily implement the benchmark. I don't know if this is how 
we want to do it, but then we can just remove the file // Albin

I added one step (p = 1) of the gates as they are defined in the paper (PHYS. REV. APPLIED 14, 034010 (2020))
I am unsure of how we define the angle for the Hadamard, I wrote 0 for now // Axel
"""
print("Done")