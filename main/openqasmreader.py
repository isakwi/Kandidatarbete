import numpy as np

from qutip import *
import qiskit

"""basic inital idea: take in qasmfile and convert the steps to a array of strings [gate1 q[n],...,] and then extract
an array that contains the order of gates being applied to qubits, use this array to determine wich gates should 
be in the same level when adding them as steps."""


circuit = qiskit.QuantumCircuit(2)
circuit.h(0)
circuit.h(0)
circuit.cx(0, 1)
circuit.h(1)
circuit.h(0)
circuit.h(1)
circuit.h(0)


"""creates text file from openqasm circuit"""
def create_file(circ):
    file = circ.qasm(formatted=True, filename='circfile.txt')

    return file


"""takes in openqasm circuit and returns array cointaining the gates in order and what qubits  
they are applied on"""

def get_arr(circ):

    file = create_file(circuit)
    with open('circfile.txt', 'r') as tx:
        str_arr = tx.readlines()
    arr = np.array(str_arr)

    return arr

array = get_arr(circuit)

"""splits string in to array of its charachters"""
def splitc(word):
    return [char for char in word]

"""function that takes in array of strings (generated from openqasm file),
and returns array of the order of wich qubits gets a gate applied on it, can be used to determine 
what gates should be in each level when they are added as steps"""

def get_qb_order(arr):
    arrc = arr[3:]
    qo_arr = []

    for stp in enumerate(arrc):
        tar =[]
        charlist= splitc(stp[1])

        for word in charlist:

            if word.isdigit():

                tar.append(int(word))

        qo_arr.append(tar)
    return qo_arr

qovec = get_qb_order(array)

print(qovec)