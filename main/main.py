""" Main program, this is the one you should run! """
import time
import matplotlib.pyplot as plt
import read_data as rd
import Qb_class as Qb
import numpy as np
import CollapseOperator_function as co
from qutip import *
import GateFuncs as gf
import main_Algorithm as mA
import benchmarking_main as bm
pi = np.pi


""" True if we are doing the benchmark! """
benchmark = False

# Parameters, eventually the number of qubits and the levels will be read from OpenQASM instead!
n, ntraj, relax, depha, therma, anharm, l = rd.read_data()  # Parameters
Qblist = []
for i in range(0, n):  # Creates list with all qubits, for now the desig and init_vec are empty
    anharm[i] = -2*pi*abs(anharm[i])*1e6  # Convert linear frequency to angular (input seems to usually be linear)
    Qblist.append(Qb.Qubit(l[i], [relax[i], depha[i], therma[i]], anharm[i], [], []))
# Parameters for gates
""" Maybe we can remove this? """
t_1q = 20e-9  # Max time for 1 qubit gate
t_2q = 200e-9  # Max time for 2 qubit gate
w_01 = 4*1e9 * 2 * pi   # Qubit frequency (4-5 GHz)
w_d = w_01
#U = -200*1e6 * 2 * pi   # Anhormonicity (only if levels > 2 ) (150-250 MHz) Moved to qb class
beta1 = pi/t_1q  # Driving strength for 1q gate
beta2 = pi/t_2q  # Driving strength for 2q gate
"""Change TimeFunc / Envelope so that it takes beta as parameter?"""


if benchmark == True:
    print("\nDoing the benchmark! :D\n")
    # Call something like benchmarking_main.py so we don't need as much code here!
    # Created a file for now
    # Should it return final state and do calculation here? Or do everything in there:
    bm.benchmarking(Qblist)

else:

    psi0 = Qb.create_psi0(Qblist)  # Create initial state with all qubits in ground state
    c_ops = co.create_c_ops(Qblist)  # Create c_ops (only relaxation and dephasing for now)
    """ Adding the algorithm steps! """
    steps = []
    steps.append(gf.Add_step(["PY","HD"], [1,2], [pi,0]))
    steps.append(gf.Add_step(["PY", "CZnew"], [0, [1, 2]], [pi/2, 0]))
    steps.append(gf.Add_step(["VPZ", "PY"], [1, 2], [pi, pi]))

    args = {"psi0": psi0, "Qblist": Qblist, "c_ops": c_ops, "steps": steps, "t_max": [t_1q, t_2q], "ntraj": ntraj}
    tic = time.perf_counter() # Start stopwatch in order to print the run time
    result = mA.main_algorithm(args)
    toc = time.perf_counter() # Stop stopwatch
    print("Done! Total mainAlgorithm run time = " + str(round(toc-tic,2)) + "s.")


    #Used for testing
    PrintStates = False
    if PrintStates:
        print(psi0)
        if type(result) == list : # Basically, if noises (mcsolve)
            print(result[-1].tidyup(atol=1e-4)) # Prints one of the final states
        elif type(result) == Qobj:
            print(result.tidyup(atol=1e-4))
        else:
            print(result.states[-1].tidyup(atol=1e-4)) # If no noises sesolve => only one state
        if len(Qblist) == 1 and Qblist[0].level == 2:
            # Bloch sphere only if 1qb 2 level
            b = Bloch()
            vec1 = psi0
            vec2 = result[-1]
            b.add_states(vec1)
            b.add_states(vec2)
            b.make_sphere()
            plt.show()