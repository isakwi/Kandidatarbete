import qnas
import qiskit
import numpy as np

circ = qiskit.QuantumCircuit(2)
circ.h(0)
circ.h(1)
circ.rx(np.pi, 0)
circ.rx(1.5*np.pi, 1)
circ.cz(0,1)

final = qnas.solve('qubitData.csv', circ, ntraj=40)