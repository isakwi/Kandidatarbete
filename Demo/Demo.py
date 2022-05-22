import qiskit
import qutip as qt
from numpy import pi
import matplotlib.pyplot as plt

import qnas

# qnas.help()

circuit = qiskit.QuantumCircuit(2)
circuit.rx(pi/2, 0)
circuit.ry(pi, 1)
circuit.cz(0, 1)

print(circuit.draw())

k02 = qt.tensor(qt.basis(3, 2), qt.basis(3, 0)) * qt.tensor(qt.basis(3, 2), qt.basis(3, 0)).dag()
e_ops = [[qt.create(3)*qt.destroy(3), 0], [qt.create(3)*qt.destroy(3), 1], [k02, [1, 0]]]

finalStates, expvals, tlist = qnas.solve(Qbfile='Demo/qubitData.csv', circuit=circuit, storeTimeDynamics=True, e_ops=e_ops)

# Plotta resultatet
plt.figure(figsize=(9.6, 7.2))
plt.plot(tlist*1e9, expvals[0], label='kvantbit 1',linewidth=3)
plt.plot(tlist*1e9, expvals[1], label='kvantbit 2',linewidth=3)
plt.plot(tlist*1e9, expvals[2], label=r'$P_{|02\rangle}$',linewidth=3)
plt.plot([0, tlist[-1]*1e9], [1, 1], '--k', linewidth=1.5)
plt.xlabel('t [ns]')
plt.ylabel('Tillstånd')
plt.legend(loc='lower right',prop={'size': 18})
plt.show()