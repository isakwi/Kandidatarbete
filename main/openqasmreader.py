import numpy as np

from qutip import *
import qiskit

"""basic inital idea: take in qasmfile and convert the steps to a array of strings [gate1 q[n],...,] and then extract
an array that contains the order of gates being applied to qubits, use this array to determine wich gates should 
be in the same level when adding them as steps."""


circuit = qiskit.QuantumCircuit(2)

def create_file(circ):
    file = circ.qasm(formatted=True, filename='circfile.txt')

    return file



def get_arr(circ):

    file = create_file(circuit)
    with open('circfile.txt', 'r') as tx:
        str_arr = tx.readlines()
    arr = np.array(str_arr)

    return arr
