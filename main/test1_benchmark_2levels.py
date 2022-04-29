import numpy as np
import gateFuncs as gf
import collapseOperatorFunction as colf
import mainAlgorithm as ma
from qutip import *
import gateLib as gl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import qubitClass as qbc
from bayes_opt import BayesianOptimization
import time



c=1000000.0
qb1 = qbc.Qubit(3, [c, c, c], -200e6 * 2 * np.pi, [1,1], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], -200e6 * 2 * np.pi, [2,2], [1,0,0])
qblist = [qb1, qb2]
c_ops = colf.createCollapseOperators(qblist)
ntraj = 3
tmax= [20e-9, 200e-9]
psi0 = qbc.createPsi0(qblist, 0)
iterations = 100
initial_points = 10

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

start_time = time.time()



#Ising hHamiltonian, our cost function is the expectation value of this hamiltonian
ham = h1 * gl.PZ(qblist, 0) + h2 * gl.PZ(qblist, 1) + J * gl.PZ(qblist, 0) * gl.PZ(qblist, 1)


def circuit(cangle1, bangle1, cangle2, bangle2):
    """ Comment from Isak: I fixed so that we don't get integration/divide by 0 error
    so I think we don't need different circuits for different problems
    ALso think that the double hadamard only is on the first level?"""
    steps = []

    if problem == 'A':
        # First level of the circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["PX"], [1], [2 * cangle1 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * cangle1 * h1, 2 * cangle1 * h2 + 0.00001]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle1, 2 * bangle1]))

        # second level of circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["PX"], [1], [2 * cangle2 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * cangle2 * h1, 2 * cangle2 * h2 + 0.0001]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle2, 2 * bangle2]))

    elif problem == 'B':
        # First level of the circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        #steps.append(gf.Add_step(["PX"], [1], [2 * cangle1 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * cangle1 * h1, 2 * cangle1 * h2 + 0.0001]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle1, 2 * bangle1]))

        # second level of circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        #steps.append(gf.Add_step(["PX"], [1], [2 * cangle2 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * cangle2 * h1, 2 * cangle2 * h2 + 0.00001]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle2, 2 * bangle2]))

    elif problem == 'C':
        # First level of the circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        #steps.append(gf.Add_step(["PX"], [1], [2 * cangle1 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * cangle1 * h1, 2 * cangle1 * h2]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle1, 2 * bangle1]))

        # second level of circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        #steps.append(gf.Add_step(["PX"], [1], [2 * cangle2 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["VPZ", "VPZ"], [0, 1], [2 * cangle2 * h1, 2 * cangle2 * h2]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle2, 2 * bangle2]))

    elif problem == 'D':
        # First level of the circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["PX"], [1], [2 * cangle1 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        #steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * cangle1 * h1, 2 * cangle1 * h2]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle1, 2 * bangle1]))

        # second level of circuit
        steps.append(gf.AlgStep(["HD", "HD"], [0, 1], [0, 0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["PX"], [1], [2 * cangle2 * J]))
        steps.append(gf.AlgStep(["CZ"], [[1, 0]], [0]))
        steps.append(gf.AlgStep(["HD"], [1], [0]))
        #steps.append(gf.Add_step(["VPZ", "VPZ"], [0, 1], [2 * cangle2 * h1, 2 * cangle2 * h2]))
        steps.append(gf.AlgStep(["PX", "PX"], [0, 1], [2 * bangle2, 2 * bangle2]))

    e_ops=[]
    # calling mainAlgorithm
    args = {"steps": steps, "c_ops": c_ops,"e_ops_inp": e_ops, "psi0": psi0, "Qblist": qblist, "t_max": tmax, "ntraj": ntraj ,"StoreTimeDynamics": False}
    state = ma.mainAlgorithm(args)

    return -np.mean(expect(ham, state))
#returns negative expectation value because Im using the maximazing function of the optimiser

upperb = np.pi
lowerb = 0
pbounds = {'cangle1': (lowerb, upperb), 'cangle2': (lowerb, upperb), 'bangle1': (lowerb, upperb), 'bangle2': (lowerb, upperb)}



new_optimizer = BayesianOptimization(
    f=circuit,
    pbounds = pbounds,
    verbose=2,
    random_state=1
)
print(new_optimizer.__class__)

new_optimizer.maximize(
    init_points= initial_points,
    n_iter= iterations,
)

print("--- %s seconds ---" % (time.time() - start_time))
print("problem:", problem, "Trajectories:" ,(ntraj), "noise:", (c), "initpoints:", (initial_points), "iterations:" ,(iterations) )
print(new_optimizer.max)
print('done')
