import qnas
import qiskit
import numpy as np

circ = qiskit.QuantumCircuit(1)
circ.rx(np.pi, 0)

final = qnas.solve('qubitData.csv',circ,)

