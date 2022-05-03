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




nlevel = 20

pi = np.pi
tstart = time.time()
c = 22220

#lists of elapsed time for number of levels and fidelities
elt_list = []
plist= []
fid_list = []
flist=[]

print("bruh1",fidelity(basis(2,0), basis(2,0)))

print("bruh2",fidelity(basis(2,0), basis(2,1)))

# qubits
qb1 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi)
qb2 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi)

c_ops_none= []
ntraj_id = 1
qblist = [qb1,qb2]
steps=[]
tot_prop=[]
c_ops = colf.createCollapseOperators(qblist)
e_ops = []
# number of trajectories
ntraj = 50
tmax= [50e-9, 271e-9]
psi0 = qbc.createPsi0(qblist, 0)  # 0 is the groundstate
initstate = tensor(basis(2,0), basis(2,0))


circ = qiskit.QuantumCircuit(2)
qc = qiskit.QuantumCircuit(2)
circ.h(0)
circ.h(1)
steps.extend(opi.qasmToQnas(circ))
qc.h(1)
qc.cz(0,1)
qc.rx(2*pi, 1)
qc.cz(0,1)
qc.h(1)
qc.id(0)
qc.rz(2*pi, 0)
qc.rz(2*pi, 1)
qc.rx(2*pi, 0)
qc.rx(2*pi,1)

onestep = opi.qasmToQnas(qc)



for p in range(0, nlevel):
    print(p+1)
    plist.append(p)
    steps.extend(onestep)
    #append(len(steps))
    tstart = time.time()

    """simulating algorithm with noise"""
    args = {"steps": steps, "c_ops": c_ops, "e_ops_inp": e_ops, "psi0": psi0, "Qblist": qblist, "t_max": tmax,
            "ntraj": ntraj, "StoreTimeDynamics": False}
    state = ma.mainAlgorithm(args)
    print(len(state))
    elt_list.append(time.time() - tstart)


    """simulating alogrithm without noise"""
    args_id = {"steps": steps, "c_ops": c_ops_none, "e_ops_inp": e_ops, "psi0": psi0, "Qblist": qblist, "t_max": tmax,
            "ntraj": ntraj_id, "StoreTimeDynamics": False}
    state_id = ma.mainAlgorithm(args_id)
    #print(state_id[0]==state_id[1], fidelity(state_id[0], state_id[1]))

    #tot_prop.extend(prop_onestp)

    """for s in enumerate(tot_prop):
        mat = mat* s[1]
"""
    #id_state = initstate * mat

    #id_denmat = id_state * id_state.dag()

    """taking mean of fidelities"""
    fmed = []

    for i in range(len(state)):
         fmed.append(fidelity(state[i], state_id))

    fid_list.append(np.mean(fmed))



print('tlist:', elt_list)
print('fidelity list:', fid_list)
print('list of corresponding levels:', plist)

fig, ax = plt.subplots()
ax.plot(plist, fid_list, label='Fidelity')
#ax.plot(plist, elt_list, label='elapsed time')
plt.show()