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
import openqasmInterpreter as opi
import qiskit
pi = np.pi
tstart = time.time()
c = 1e-1 * 1
storeData = False
# qubits
qb1 = qbc.Qubit(3, [c, c, 0], -229e6 * 2 * pi)
qb2 = qbc.Qubit(3, [c, c, 0], -225e6 * 2 * pi)
betaplot = False #make this true if we want 1D plots as well


# list of angles for parameters


qblist = [qb1, qb2]

c_ops = colf.createCollapseOperators(qblist)
e_ops = []
# number of trajectories
ntraj = 20
tmax= [50e-9, 271e-9]
psi0 = qbc.createPsi0(qblist, 0)  # 0 is the groundstate
problem = 'c'

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


def ourcirc(gamma, beta):

    circ = qiskit.QuantumCircuit(2)
    circ.h(0)
    circ.h(1)
    circ.id(0)
    circ.h(1)
    circ.cz(1,0)
    circ.id(0)
    circ.rx(2*gamma*J, 1)
    circ.cz(1,0)
    circ.h(1)
    circ.id(0)
    circ.rz(2*gamma*h1, 0)
    circ.rz(2*gamma*h2, 1)
    circ.rx(2*beta, 0)
    circ.rx(2*beta,1)
    return circ


# Ising hHamiltonian, our cost function is the expectation value of this hamiltonian
ham = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)  # Maybe plus/minus


# iterating through list of angles and saving expectation values in matrix
beta, gamma = np.pi/4, np.pi/4
steps = opi.qasmToQnas(ourcirc(gamma, beta))
        #print(f"steps: {[step.name for step in steps]} targets : {[step.Tar_Con for step in steps]}, angles: {[step.angle for step in steps]} ")
# calling mainAlgorithm
e_entang0 = [-1j * (destroy(3) - create(3)),0]
e_entang1 = [-1j * (destroy(3) - create(3)),1]
k11 = tensor(basis(3, 1), basis(3, 1))
k00 = tensor(basis(3, 0), basis(3, 0))
k01 = tensor(basis(3, 0), basis(3, 1))
k10 = tensor(basis(3, 1), basis(3, 0))

e_entangplus = [0.25 * (k00+k01+k10+k11)*(k00+k01+k10+k11).dag(),0]
e_entangminus = [0.25 * (k00+k01+k10-k11)*(k00+k01+k10-k11).dag(),0]
e_ops_inp = [[basis(3,0)*basis(3,0).dag(),0],[basis(3,0)*basis(3,0).dag(),1],[basis(3,1)*basis(3,1).dag(),0],[basis(3,1)*basis(3,1).dag(),1],[basis(3,2)*basis(3,2).dag(),0],[basis(3,2)*basis(3,2).dag(),1]]
e_ops_inp.append(e_entang0)
e_ops_inp.append(e_entang1)
e_ops_inp.append(e_entangplus)
e_ops_inp.append(e_entangminus)
args = {"steps" : steps, "c_ops" : c_ops, "e_ops_inp": e_ops_inp, "psi0" : psi0, "Qblist": qblist, "t_max": tmax, "ntraj" : ntraj, "StoreTimeDynamics": True}
state, expval, tlist = ma.mainAlgorithm(args)
# saving mean value of expectation value in matrix

print("Time elapsed: %.2f seconds." %(time.time()-tstart))

# plotting matrix
# plt.matshow(exp_mat, cmap = plt.get_cmap('PiYG'))  # We need to flip the matrix of we use the matshow
# Do this by putting exp_mat[beta_resolution-1-j, i] = np.mean(expect(ham, state)) in for loops!) !
fig, ax = plt.subplots()
#cs = ax.contourf(gamma_vec, beta_vec, exp_mat, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
# This one plots the matrix with angles
#cbar = fig.colorbar(cs, ticks=np.linspace(-1,1,9))
#ax.set_title(f'Cost function F($\gamma$, \u03B2) for problem {problem}')
#ax.set_xlabel("$\gamma_1$")
#ax.set_ylabel("\u03B2$_1$")
#labels = ["0", "$\pi$/2", "$\pi$"]
#plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
#plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
#ax.plot(tlist, np.abs(expval[0]) )
#ax.plot(tlist, np.abs(expval[2]) )

#ax.plot(tlist,np.abs(expval[0]) *  np.abs(expval[1]) ) #|00>
#ax.plot(tlist,np.abs(expval[0]) *  np.abs(expval[3]) )#|01>
#ax.plot(tlist,np.abs(expval[0]) *  np.abs(expval[5]) )#|02>
#ax.plot(tlist,np.abs(expval[2]) *  np.abs(expval[1]) )#|10>
#ax.plot(tlist,np.abs(expval[2]) *  np.abs(expval[3]) )#|11>
#ax.plot(tlist,np.abs(expval[2]) *  np.abs(expval[5]) )#|12>
#ax.plot(tlist,np.abs(expval[4]) *  np.abs(expval[1]) )#|20>
#ax.plot(tlist,np.abs(expval[4]) *  np.abs(expval[3]) )#|21>
#ax.plot(tlist,np.abs(expval[4]) *  np.abs(expval[5]) )#|22>
#ax.plot(tlist,np.abs(expval[0]) +  np.abs(expval[2]) + np.abs(expval[4]) )
ax.plot(tlist,(expval[0]*expval[5]))
ax.plot(tlist,(expval[8]))
ax.plot(tlist,(expval[9]))
plt.show()


# Find minima manually, will be fast for small matrices, like in the benchmark!
# Only finds one minimum though, not if there are many


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

    #saves in the current directory, you can add a path before the name: "path/betaplot"...
    imStr = "betaplot" + str(problem).upper() + ".pdf"
    plt.show()
    fig.savefig(imStr, format="pdf", bbox_inches="tight")
"""
This is meant to be a file to easily implement the benchmark. I don't know if this is how 
we want to do it, but then we can just remove the file // Albin

I added one step (p = 1) of the gates as they are defined in the paper (PHYS. REV. APPLIED 14, 034010 (2020))
I am unsure of how we define the angle for the Hadamard, I wrote 0 for now // Axel
"""

if storeData:
    with np.printoptions(threshold=np.inf):
        file = open("expValuesData.txt", "w+") #Seems to work
        file.write(f"P(qubit_1 = |0>: \n {expval[0]}")
        file.close()

print("\nDone")