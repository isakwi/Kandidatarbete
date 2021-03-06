import numpy as np
from qutip.qip.circuit import QubitCircuit

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



c = 1000

#lists of elapsed time for number of levels and fidelities
elt_list = []
plist= []
nlist = []
flist=[]

ntraj = 100
e_ops=[]
tmax= [50e-9, 271e-9]



# qubits
qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * np.pi)


def circuit(N):

    circ = qiskit.QuantumCircuit(N)

    for n in range(0,N): #hadamar on all qubits
        circ.h(n)
    if N > 3:
        for k in range(0,N):
            u = 2*k +1


            if u < N-1:
                circ.cz(u, u+1)

        for k in range(0,N):
            J = 2*k
            if J +1< N:
                circ.cz(J, J + 1)

    elif N == 2:
        circ.cz(0,1)
    elif N == 3:
        circ.cz(0,1)
        circ.cz(1,2)

    for n in range(0, N):
        circ.h(n)

    for n in range(0, N):
        circ.rx(2*np.pi,n)

    for n in range(0, N):
        circ.ry(np.pi, n)

    for n in range(0, N):
        circ.rx(np.pi, n)

    if N > 3:
        for k in range(0,N):
            u = 2*k +1


            if u < N-1:
                circ.cz(u, u+1)

        for k in range(0,N):
            J = 2*k
            if J +1< N:
                circ.cz(J, J + 1)

    elif N == 2:
        circ.cz(0,1)
    elif N == 3:
        circ.cz(0,1)
        circ.cz(1,2)

    for n in range(0, N):
        circ.rx(np.pi,n)

    for n in range(0, N):
        circ.ry(np.pi, n)

    for n in range(0, N):
        circ.rx(np.pi, n)
    return circ


ant = 15






for it in range(2, ant):
    nlist.append(it)
    #print(circuit(it))

    qblist= [qb1]* it

    steps = opi.qasmToQnas(circuit(it))
    #print(steps)

    c_ops = colf.createCollapseOperators(qblist)
    psi0 = qbc.createPsi0(qblist, 0)  # 0 is the groundstate

    args = {"steps": steps, "c_ops": c_ops, "e_ops_inp": e_ops, "psi0": psi0, "Qblist": qblist, "t_max": tmax,
            "ntraj": ntraj, "StoreTimeDynamics": False}

    tstart = time.time()

    state = ma.mainAlgorithm(args)
    elt_list.append(time.time()-tstart)
    print(len(state))
    print('elt_list=',elt_list, nlist, "state=", state[0].dims, state[0].shape)


print('ntraj=', ntraj)


























