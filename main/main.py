""" Main program, this is the one you should run!"""

import read_data as rd
import Qb_class as Qb

# Parameters, eventually the number of qubits and the levels will be read from OpenQASM instead!
n, relax, depha, inter, therma, l = rd.read_data()  # Parameters
Qblist = []
for i in range(0, n):  # Creates list with all qubits
    Qblist.append(Qb.Qubit(l[i], [relax[i], depha[i], inter[i], therma[i]], [], []))


