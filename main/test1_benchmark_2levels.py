import numpy as np
import GateFuncs as gf
import CollapseOperator_function as colf
import main_Algorithm as ma
from qutip import *
import GateLib as gl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import Qb_class as qbc
from bayes_opt import BayesianOptimization



c=0.001
qb1 = qbc.Qubit(3, [c, c, c], 0.1, [1,1], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], 0.1, [2,2], [1,0,0])
qblist = [qb1, qb2]
c_ops = colf.create_c_ops(qblist)
ntraj = 1
tmax= [20, 200]
psi0 = qbc.create_psi0(qblist)

problem = 'A'

if problem == 'A':
    J = 1
    h1, h2 = -0.5, 0
elif problem == 'B':
    J = 0
    h1, h2 = -1.0, 0
elif problem == 'C':
    J = 0
    h1, h2 = -0.5, -0.5
elif problem == 'D':
    J = 1
    h1, h2 = 0, 0




#Ising hHamiltonian, our cost function is the expectation value of this hamiltonian
ham = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)


def circuit(cangle1, bangle1, cangle2, bangle2):
    steps = []
    # First level of the circuit
    steps.append(gf.Add_step(["HD", "HD"], [0, 1], [0, 0]))
    steps.append(gf.Add_step(["HD"], [1], [0]))
    steps.append(gf.Add_step(["CZnew"], [[1, 0]], [0]))
    steps.append(gf.Add_step(["PX"], [1], [2 * cangle1 * J]))
    steps.append(gf.Add_step(["CZnew"], [[1, 0]], [0]))
    steps.append(gf.Add_step(["HD"], [1], [0]))
    steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * cangle1 * h1, 2 * cangle1 * h2]))
    steps.append(gf.Add_step(["PX", "PX"], [0, 1], [2 * bangle1, 2 * bangle1]))

    #second level of circuit
    steps.append(gf.Add_step(["HD", "HD"], [0, 1], [0, 0]))
    steps.append(gf.Add_step(["HD"], [1], [0]))
    steps.append(gf.Add_step(["CZnew"], [[1, 0]], [0]))
    steps.append(gf.Add_step(["PX"], [1], [2 * cangle2 * J]))
    steps.append(gf.Add_step(["CZnew"], [[1, 0]], [0]))
    steps.append(gf.Add_step(["HD"], [1], [0]))
    steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * cangle2 * h1, 2 * cangle2 * h2]))
    steps.append(gf.Add_step(["PX", "PX"], [0, 1], [2 * bangle2, 2 * bangle2]))

    # calling main_algorithm
    args = {"steps": steps, "c_ops": c_ops, "psi0": psi0, "Qblist": qblist, "t_max": tmax, "ntraj": ntraj}
    state = ma.main_algorithm(args)

    return np.mean(expect(ham, state))


pbounds = {'cangle1': (0, np.pi), 'cangle2': (0, np.pi), 'bangle1': (0, np.pi), 'bangle2': (0, np.pi)}



new_optimizer = BayesianOptimization(
    f=circuit,
    pbounds=pbounds,
    verbose=2,
    random_state=1
)
print(new_optimizer.__class__)
