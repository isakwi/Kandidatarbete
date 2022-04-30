import numpy as np
import gateFuncs as gf
import collapseOperatorFunction as colf
import mainAlgorithm as ma
#import main_Alg_parfortest as ma  #Uncomment to change to parfor from the start
from qutip import *
import gateLib as gl
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import qubitClass as qbc
import matplotlib as mpl
pi = np.pi
tstart = time.time()
c = 0.00

T1qb1 = 77e-6 #relaxation time
T1qb2 = 55e-6

T2qb1 = 49e-6 #free induction decay time (dephasing?)
T2qb2 = 82e-6

Tphiqb1 = 1/(1/T2qb1 - 1/(2 * T1qb1)) # Pure dephasing
Tphiqb2 = 1/(1/T2qb2 - 1/(2 * T1qb2))

"""Calculate rates"""
G1qb1 = 1/T1qb1
G1qb2 = 1/T1qb2

Gphiqb1 = 1/Tphiqb1
Gphiqb2 = 1/Tphiqb2

# qubits
#qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
#qb2 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])
qb1 = qbc.Qubit(3, [G1qb1, Gphiqb1, c], -229e6 * 2 * pi) # In other parts of the program we work linearly, right? Should be angular, So this is correct. Input in .csv is linear
qb2 = qbc.Qubit(3, [G1qb2, Gphiqb2, c], -225e6 * 2 * pi)

zz_mat = [[0, 2*pi*1e5], [0, 2*pi*1e5]]

betaplot = True #make this true if we want 1D plots as well
storeData = True  # To store data in a txt file

gamma_resolution = 60
beta_resolution = 60

# list of angles for parameters
gamma_vec = np.linspace(0, pi, gamma_resolution)
beta_vec = np.linspace(0, pi, beta_resolution)
qblist = [qb1, qb2]

# zeros matrix for saving expectation value of hamiltonian
exp_mat = np.zeros((beta_resolution, gamma_resolution))
if betaplot:
    state_mat = [[qeye(1) for i in range(gamma_resolution)] for j in range(beta_resolution)]
c_ops = colf.createCollapseOperators(qblist)
# number of trajectories
ntraj = 500
tmax= [50e-9, 271e-9]
psi0 = qbc.createPsi0(qblist, 0)  # 0 is the groundstate
problem = 'b'

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
steps = [gf.AlgStep(["PX"], [1], [0.1]) for i in range(8)]  # zero angle rotation, will all be replaced

steps[0] = (gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))  # First we apply Hadamard to both qubits
steps[1] = (gf.AlgStep(["HD"], [1], [0]))  # Then we apply Hadamard to the second qubit
steps[2] = (gf.AlgStep(["CZ"], [[1, 0]], [0]))
steps[4] = (gf.AlgStep(["CZ"], [[1, 0]], [0]))


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
        steps[3] = (gf.AlgStep(["PX"], [1], [2 * gamma * J]))
        steps[5] = (gf.AlgStep(["HD"], [1], [0]))
        steps[6] = (gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * gamma * h1, 2 * gamma * h2]))
        steps[7] = (gf.AlgStep(["PX", "PX"], [0, 1], [2 * beta, 2 * beta]))
# calling mainAlgorithm
        #print(f"steps: {[step.name for step in steps]} targets : {[step.Tar_Con for step in steps]}, angles: {[step.angle for step in steps]} ")
        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": qblist, "t_max": tmax, "ntraj" : ntraj, "StoreTimeDynamics": False, "zz_mat":zz_mat}
        args["e_ops_inp"] = []
        state = ma.mainAlgorithm(args)
# saving mean value of expectation value in matrix
        exp_mat[j, i] = np.mean(expect(ham, state))  # Beta y-axis and gamma x-axis
        if betaplot:
            state_mat[j][i] = state[0].data

print("Time elapsed: %.2f seconds." %(time.time()-tstart))

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

if storeData:
    with np.printoptions(threshold=np.inf):
        file = open("plotdata_" + problem + ".txt", "w+") #Seems to work
        file.write("For contourf:" + '\n' + "gamma_vec = " + str(gamma_vec) + '\n' + "beta_vec = " + str(beta_vec) + '\n' "exp_mat = " + str(exp_mat) + '\n' "minima = " + str(minima) + '\n' "coord = " + str(coord) + '\n')
        file.close()

if betaplot:
    fig, ax2 = plt.subplots()
    state_vec = [row[coord[1]] for row in state_mat]
    cost_vec = [cost[coord[1]] for cost in exp_mat]
    zz = [state[0,0] for state in state_vec]  # |00>
    zz = [np.abs(amp) ** 2 for amp in zz]
    zo = [state[1,0] for state in state_vec]  # |01>
    zo = [np.abs(amp) ** 2 for amp in zo]
    oz = [state[3,0] for state in state_vec]  # |10>
    oz = [np.abs(amp) ** 2 for amp in oz]
    oo = [state[4,0] for state in state_vec]  # |11>
    oo = [np.abs(amp) ** 2 for amp in oo]
    ax2.plot(beta_vec, cost_vec, 'o',color = "magenta", label="F")
    ax2.plot(beta_vec, zz, 'o',color = "orange", label="P(|00>)")
    ax2.plot(beta_vec, zo, 'ro', label="P(|01>)")
    ax2.plot(beta_vec, oz, 'go', label="P(|10>)")
    ax2.plot(beta_vec, oo, 'o',color = "purple",  label="P(|11>)")
    ax2.legend()
    ax2.set(xlim= (0,pi), ylim= (-1, 1))
    #Title if you want, uncomment then
    #ax2.set_title('Problem {problem}')
    ax2.set_xlabel(r"$\beta$")
    ax2.set_ylabel("Cost function or probability of occupation")
    file = open("plotdata_" + problem + ".txt", "a") #Seems to work
    file.write("For betaplot:" + '\n' + "beta_vec = " + str(beta_vec) + '\n')
    file.write("zz = " + str(zz) + '\n')
    file.write("zo = " + str(zo) + '\n')
    file.write("oz = " + str(oz) + '\n')
    file.write("oo = " + str(oo) + '\n')
    file.close()

    #saves in the current directory, you can add a path before the name: "path/betaplot"...
    imStr = "betaplot" + str(problem).upper() + "FOR_PROGRAM.pdf"
    plt.show()
    fig.savefig(imStr, format="pdf", bbox_inches="tight")
"""
This is meant to be a file to easily implement the benchmark. I don't know if this is how 
we want to do it, but then we can just remove the file // Albin

I added one step (p = 1) of the gates as they are defined in the paper (PHYS. REV. APPLIED 14, 034010 (2020))
I am unsure of how we define the angle for the Hadamard, I wrote 0 for now // Axel
"""
print("\nDone")
