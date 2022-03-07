""" Main program, this is the one you should run!"""

import read_data as rd
import Qb_class as Qb
import numpy as np

# Parameters, eventually the number of qubits and the levels will be read from OpenQASM instead!
n, relax, depha, inter, therma, l = rd.read_data()  # Parameters
Qblist = []
for i in range(0, n):  # Creates list with all qubits, for now the desig and init_vec are empty
    Qblist.append(Qb.Qubit(l[i], [relax[i], depha[i], inter[i], therma[i]], [], []))

# Parameters for gates
t_1q = 20e-9  # Max time for 1 qubit gate
t_2q = 200e-9  # Max time for 2 qubit gate
w_01 = 4*1e9 * 2 * np.pi   # Qubit frequency (4-5 GHz)
w_d = w_01
U = -200*1e6 * 2 * np.pi   # Anhormonicity (only if levels > 2 ) (150-250 MHz)
beta1 = np.pi/t_1q  # Driving strength for 1q gate
beta2 = np.pi/t_2q  # Driving strength for 2q gate
"""Change TimeFunc / Envelope so that it takes beta as parameter?"""
