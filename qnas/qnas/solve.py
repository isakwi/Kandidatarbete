#import openqasmreader as oqread
from . import GateFuncs as gf
from . import Qb_class as qbc
import numpy as np
from . import read_data as rd
from . import CollapseOperator_function as co
from . import main_Algorithm as ma
from qutip import *

def solve(Qbfile = None, OpenQASM = None, int_matrix = None, ntraj=500, tmax=None, store_time_dynamics = False, e_ops=None):
    """
    The main solver function. Basically a user calls this function and everything else is automatic
    :param Qbfile: File that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi
    :param OpenQASM: File that specifies OpenQASM file. Default - Asks user to specify gates manually or not run
    :param int_matrix: 15x15 matrix that describes interaction between qubits
    :param ntraj: number of trajectories for the Monte Carlo solver. Default - 500
    :param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9]
    :param store_time_dynamics: True/False value to store time dynamics. Default - False
    :param e_ops: Expectation value operators for store_time_dynamics. Given as [[e_op1, Tar_Con],[e_op2, Tar_Con], ...]
    :return: if store_time_dynamics is True: Returns ntraj many final states and two lists with exp values
            and corrrespnding timrs. Else: ntraj many final states
    """
    if e_ops is None:
        e_ops = []
    if OpenQASM is None:
        print("You didn't enter an OpenQASM circuit. QnAS will now exit?\t")
        return

    try:  # Input can either be openqasm file or qiskit circuit? Add functionality for that
        #steps = oqread.FUNCTION(Qbfile)  # Should return a list with Add_step objects?
        print("Reading OpenQASM file is not implemented yet!")
        steps = [gf.Add_step(["PX", "CZnew"], [0, [0,1]], [np.pi, 0])]  # Temporary steps to not get syntax errors everywhere
    except:
        print(f"Couldn't read the OpenQASM file! Check that the filename, {OpenQASM}, is correct and that the file is "
              "constructed correctly. QnAS.solve() will now exit")
        return

    # Check n
    maxn = -1
    for step in steps:
        for target in step.Tar_Con:
            if type(target) == int:
                if target > maxn:
                    maxn = target
            elif type(target) == list:
                if max(target) > maxn:
                    maxn = target
    if maxn == -1:
        print("No qubit has been targeted by the algorithm, number of qubits could not be decided."
                " QnAS.solve() will now exit")
        return
    else:
        n = maxn + 1

    if not  (1 <= n <= 15 and n <= maxn+1):
        print("Invalid value for number of qubits! Must be between 1 and 15! QnAS.solve() will now exit")
        return

    # Read qubit parameters
    if Qbfile is None:
        print("You didn't specify a file for the qubit parameters! \n"
              "QnAS assumes you have 3 levels, no noises and sets the anharmonicity to"
              " -225e6*2*pi for all qubits")
        Qblist = [qbc.Qubit(3, [0,0,0], -225e6 * 2 * np.pi, [], []) for i in range(n)]
    else:
        try:
            relax, depha, therma, anharm, levels = rd.readfile(Qbfile)
            Qblist = []
        except:
            print(f"Couldn't find file {Qbfile}. QnAS.solve() will now exit")
            return
        for i in range(0, n):  # Creates list with all qubits, for now the desig and init_vec are empty
            anharm[i] = -2 * np.pi * abs(anharm[i]) * 1e6  # Convert linear frequency to angular (input seems to usually be linear)
            Qblist.append(qbc.Qubit(levels[i], [relax[i], depha[i], therma[i]], anharm[i], [], []))

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


    if type(int_matrix) != list:
        print("Wrong format for the interaction matrix! Should be given as [[x1, x2, ... , x15], [...]]"
              "\nand be of size 15x15! QnAS.solve() will now exit")
        return
    if len(int_matrix) != 15:
        print("The matrix is not 15x15! QnAS.solve() will now exit")
        return
    for row in int_matrix:
        if len(row) != 15:
            print("The matrix is not 15x15! QnAS.solve() will now exit")
            return

    psi0 = qbc.create_psi0(Qblist, 0)
    c_ops = co.create_c_ops(Qblist)

    if int_matrix is None:
        args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": Qblist, "t_max": tmax, "ntraj" : ntraj,
                "StoreTimeDynamics": store_time_dynamics, "e_ops_inp": e_ops}

    else:
        args = {"steps": steps, "c_ops": c_ops, "psi0": psi0, "Qblist": Qblist, "t_max": tmax, "ntraj": ntraj,
                "StoreTimeDynamics": store_time_dynamics, "e_ops_inp": e_ops, "zz_mat": int_matrix}

    return ma.main_algorithm(args)
