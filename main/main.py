""" Main program, this is the one you should run! """

import read_data as rd
import Qb_class as Qb
import numpy as np
import CollapseOperator_function as co
from qutip import *
import GateFuncs as gf
import main_Algorithm as mA
pi = np.pi

# Parameters, eventually the number of qubits and the levels will be read from OpenQASM instead!
n, relax, depha, inter, therma, l = rd.read_data()  # Parameters
Qblist = []
for i in range(0, n):  # Creates list with all qubits, for now the desig and init_vec are empty
    Qblist.append(Qb.Qubit(l[i], [relax[i], depha[i], inter[i], therma[i]], [], []))

# Parameters for gates
t_1q = 20e-9  # Max time for 1 qubit gate
t_2q = 200e-9  # Max time for 2 qubit gate
w_01 = 4*1e9 * 2 * pi   # Qubit frequency (4-5 GHz)
w_d = w_01
U = -200*1e6 * 2 * pi   # Anhormonicity (only if levels > 2 ) (150-250 MHz)
beta1 = pi/t_1q  # Driving strength for 1q gate
beta2 = pi/t_2q  # Driving strength for 2q gate
"""Change TimeFunc / Envelope so that it takes beta as parameter?"""


def create_psi0(Qblist):
    """ If the initial states are always 0 for all qubits it might be easier
        to not have it in the Qubit-class and just have something like this!
        Can be added to another file to keep things in "main" nice and tidy!

        Creates initial state with all qubits in state 0: """
    psi0 = [basis(Qb.level, 0) for Qb in Qblist]
    return tensor(psi0)


psi0 = create_psi0(Qblist)  # Create initial state with all qubits in ground state
c_ops = co.create_c_ops(Qblist)  # Create c_ops (only relaxation and dephasing for now)

""" Adding the algorithm steps! """
steps = []
steps.append(gf.Add_step(["CZ"], [[0, 1]], [pi]))
steps.append(gf.Add_step(["PX", "PY"], [0, 1], [pi, pi/2]))
steps.append(gf.Add_step(["PX", "HD"], [0, 1], [pi, 0]))

args = {"psi0": psi0, "Qblist": Qblist, "c_ops": c_ops, "steps": steps, "U": U}
result = mA.main_algorithm(args)
print("Done!")
