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



c = 0.01

#lists of elapsed time for number of levels and fidelities
elt_list = []
plist= []
fid_list = []
flist=[]

N=5


# qubits
qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * np.pi, [1,1], [1,0,0])


def circuit(N):

    circ= qiskit.QuantumCircuit(N)

    for n in range(0,N):
        circ.h(n)
    if N > 3:
        for k in range(0,N):
            u = 2*k +1


            if u < N:
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
        circ.ry(2 * np.pi, n)

    for n in range(0, N):
        circ.rx(2 * np.pi, n)

    if N > 3:
        for k in range(0,N):
            u = 2*k +1


            if u < N:
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
        circ.rx(2*np.pi,n)

    for n in range(0, N):
        circ.ry(2 * np.pi, n)

    for n in range(0, N):
        circ.rx(2 * np.pi, n)


qblist = [qb1] * N


























