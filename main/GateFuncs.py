"""
Definition of functions:
- CreateGates (Gate, target, NoOfGates, QbLevel) - > Tensored operator where gate acts on correct qubit
- TimeDependGates (tlist) - > QobjEvo of time dependant gate with correct drive interval
- AddGates ( QobjEvo ) - > Adds QobjEvos to final Hamiltonian

"""

import GateLib
from qutip import *
import numpy as np 

""" 
Function for generating general operators given the number of qubits (n), the number of energy levels (L), 
which gate (G) one wants to apply and which qubit (i) the gate should act on. Note that indexing starts on 0. 
"""
def single_qubit_gate(n, L, G, i):
    x = [qeye(L) for x in range(n)]
    x[i] = G(L)
    return tensor(x)

"Function that creates annihilation operators for a given qubit"
def annihilation(n,L,i):
    return single_qubit_gates(n,L,destroy,i) 


"For future reference, Add Gates could probably be written on this sort of form"
# H = H_anh
# for i in len(gate):
#     H= H + QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)