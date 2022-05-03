import qnas
import qiskit as qk
from numpy import pi

n = 1
circuit = qk.QuantumCircuit(n)
circuit.rx(0, 0)

result = qnas.solve(Qbfile='qubitData.csv', circuit=circuit)
