#import openqasmreader as oqread
from . import gateFuncs as gf
from . import qubitClass as qbc
import numpy as np
from . import readData as rd
from . import collapseOperatorFunction as co
from . import mainAlgorithm
from . import openqasmInterpreter as opq
from qutip import *
def solve(Qbfile = None, circuit = None, zz_int = None, ntraj=500, tmax=None, store_time_dynamics = False, e_ops=None):
    """
    The main solver function. Basically a user calls this function and everything else is automatic
    :param Qbfile: File that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi
    :param circuit: Qiskit QuantumCircuit object to specify quantum circuit. Can't run without
    :param zz_int: symmetrical square (n x n) matrix that describes interaction between qubits
    :param ntraj: number of trajectories for the Monte Carlo solver. Default - 500
    :param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9]
    :param store_time_dynamics: True/False value to store time dynamics. Default - False
    :param e_ops: Expectation value operators for store_time_dynamics. Given as [[e_op1, Tar_Con],[e_op2, Tar_Con], ...]
    :return: if store_time_dynamics is True: Returns ntraj many final states and two lists with exp values
            and corresponding times. Else: ntraj many final states
    """
    if e_ops is None:
        e_ops = []
    if circuit is None:
        print("You didn't enter an circuit circuit. QnAS will now exit?\t")
        return

    try:  # Input can either be openqasm file or qiskit circuit? Add functionality for that
        steps = opq.qasmToQnas(circuit)
    except:
        print(f"Couldn't read the circuit file! Check that the circuit, {circuit}, is correct and that the circuit is"
              "constructed correctly. \nQnAS.solve() will now exit")
        return

    # Check n
    # Think this will work instead
    try:
        n = circuit.num_qubits
    except:
        print("Couldn't determine number of qubits from circuit."
              "\nQnAS.solve() will now exit")

    if not 1 <= n <= 15:
        print("Invalid value for number of qubits! Must be between 1 and 15! \nQnAS.solve() will now exit")
        return

    # Read qubit parameters
    if Qbfile is None:
        print("You didn't specify a file for the qubit parameters! \n"
              "QnAS assumes you have 3 levels, no noises and sets the anharmonicity to"
              " -225e6*2*pi for all qubits")
        Qblist = [qbc.Qubit(3, [0,0,0], -225e6 * 2 * np.pi) for i in range(n)]
    else:
        try:
            relax, depha, therma, anharm, levels = rd.readFile(Qbfile, n)
            Qblist = []
        except:
            print(f"Couldn't find file {Qbfile}. QnAS.solve() will now exit")
            return
        for i in range(0, n):  # Creates list with all qubits, for now the desig and init_vec are empty
            anharm[i] = -2 * np.pi * abs(anharm[i]) * 1e6  # Convert linear frequency to angular (input seems to usually be linear)
            Qblist.append(qbc.Qubit(levels[i], [relax[i], depha[i], therma[i]], anharm[i]))

    if not 1 <= ntraj <= 100000:
        print("Invalid value for ntraj! Must be a positive integer with an upper limit of 100000 (to not kill your"
              " computer). If you leave it unspecified, ntraj will automatically be 500. QnAS.solve() will now exit")
        return

    if tmax is None:
        print("No input for tmax! QnAS will use 1qb gate time: 20ns and 2qb gate time: 200ns!")
        tmax = [20e-9, 200e-9]

    if not type(tmax) == list:
        print("Invalid input for tmax! tmax must be a list of the form [1qb, 2qb] with "
              "max gate times for 1-qubit-gates and 2-qubit-gates given in seconds!"
              " QnAS.solve() will now exit")
        return
    if not (1e-12 < tmax[0] < 1e12 or 1e-12 < tmax[1] < 1e12):
        print("Invalid values for at least one of the max gate times. Limits are 1e-12 < t < 1e12. "
              " QnAS.solve() will now exit")
        return
    if type(store_time_dynamics) != bool:
        print("store_time_dynamics must be a boolean (True/False). "
              "QnAS.solve() will now exit")
        return
    if store_time_dynamics == True:  # Only need to check e_ops if store_td is true
        if e_ops is None:
            print("You didn't enter any e_ops, no need to save time dynamics!")
            store_time_dynamics = False
        if type(e_ops) != list:
            print("Wrong input type of e_ops! Input given on the form:\n"
                  "e_ops_inp = [[e_op1, Tar_Con],[e_op2, Tar_Con], ... ]\n"
                  "where e_op is a Qobj with the dimensions  ( qubit.level x qubit.level )\n"
                  "and Tar_Con is the target and control in case of 2qb gate, as before.\n"
                  "QnAS.solve() will now exit")
            return
        for e_op in e_ops:
            if type(e_op) != list:
                print("Wrong input type of e_ops! Input given on the form:\n"
                      "e_ops_inp = [[e_op1, Tar_Con],[e_op2, Tar_Con], ... ]\n"
                      "where e_op is a Qobj with the dimensions  ( qubit.level x qubit.level )\n"
                      "and Tar_Con is the target and control in case of 2qb gate, as before.\n"
                      "QnAS.solve() will now exit")
                return
            #if type(e_op[0]) != Qobj:  # Would like to add something like this but don't know how

    if zz_int is not None:
        if type(zz_int) != list:
            print("Wrong format for the interaction matrix! Should be given as [[x1, x2, ... , xn], [...]]"
                  "\nfor n qubits! QnAS.solve() will now exit")
            return
        if not n <= len(zz_int) <= 15:
            print("The matrix can't be smaller than the number of qubits (or larger than 15)! \n"
                  "QnAS.solve() will now exit")
            return
        for row in zz_int:
            if not n <= len(row) <= 15:
                print("The matrix can't be smaller than the number of qubits (or larger than 15)!\n "
                      "QnAS.solve() will now exit")
                return

    psi0 = qbc.createPsi0(Qblist, 0)
    c_ops = co.createCollapseOperators(Qblist)

    if zz_int is None:
        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": Qblist, "t_max": tmax, "ntraj" : ntraj,
                "StoreTimeDynamics": store_time_dynamics, "e_ops_inp": e_ops}

    else:
        args = {"steps": steps, "c_ops": c_ops, "psi0": psi0, "Qblist": Qblist, "t_max": tmax, "ntraj": ntraj,
                "StoreTimeDynamics": store_time_dynamics, "e_ops_inp": e_ops, "zz_mat": zz_int}

    return mainAlgorithm(args)
