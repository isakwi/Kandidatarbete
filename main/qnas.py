"""
File to import, here comes the user-friendliness
"""
#import openqasmreader as oqread
import Qb_class as qbc
import GateFuncs as gf
import numpy as np
import read_data as rd
import CollapseOperator_function as co
import main_Algorithm as ma

def help():
    """
    User calls this function to recieve information about how to use QnAS
    """

    print("\n\nHello, welcome to QnAS - Quantum noisy Algorithm simulator!\n"
          "Here comes some help on how to get started :)\n\n"
          "The program is made to be able to simulate quantum algorithms, with noise,"
          " from the gates available at WACQT. All gates available are:\n"
          "\"PX\" Pauli x gate\n"
          "\"PY\" Pauli y gate\n"
          "\"VPZ\" Pauli z gate but this one is virtual, takes no time, hence the V in in VPZ\n"
          "\"HD\" Hadamard gate\n"
          "\"CZ\" Controlled z gate\n"
          "\"iSWAP\" iSWAP gate\n"
          "Make sure these are the only gates you have included in your OpenQASM file to create the algorithm!\n"
          "\nDescription of functions: \n\n"
          "help()\n"
          ":You already called this function so you probably know that "
          "it just helps you get started!\n\n"
          "solve(Qbfile, OpenQASM, n, ntraj, tmax, store_time_dynamics)\n"
          ":param Qbfile: Filepath that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi\n"
          ":param OpenQASM: Filepath that specifies OpenQASM file. Default - Asks user to specify gates manually or not run\n"
          ":param n: number of qubits. Default - Last qubit targeted by OpenQASM\n"
          ":param ntraj: number of trajectories for the Monte Carlo solver. Default - 500\n"
          ":param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9]\n"
          ":param store_time_dynamics: True/False value to store time dynamics. Default - False\n"
          ":return: if store_time_dynamics is True: Not sure yet. Else: ntraj many final states\n\n")


def solve(Qbfile = None, OpenQASM = None, n=None, ntraj=500, tmax=None, store_time_dynamics = False):
    """
    The main solver function. Basically a user calls this function and everything else is automatic
    :param Qbfile: File that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi
    :param OpenQASM: File that specifies OpenQASM file. Default - Asks user to specify gates manually or not run
    :param n: number of qubits. Default - Last qubit targeted by OpenQASM
    :param ntraj: number of trajectories for the Monte Carlo solver. Default - 500
    :param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9]
    :param store_time_dynamics: True/False value to store time dynamics. Default - False
    :return: if store_time_dynamics is True: Not sure yet. Else: ntraj many final states
    """
    if tmax is None:
        tmax = [20e-9, 200e-9]
    if OpenQASM is None:
        print("You didn't enter an OpenQASM file. Do you want to add gates manually ('y'/'n')?\t")
        inp = input()
        if inp == 'y':
            # Call some function which makes the user manually input gates
            print("This has not been implemented yet, sorry! Try specifying an OpenQASM file instead."
                  " QnAS.solve() will now exit")
            return
        elif inp == 'n':
            print("Okay! Try specifying an OpenQASM file. QnAS.solve() will now exit")
            return
        else:
            print("You didn't enter 'y' or 'n', QnAS.solve() will now exit")
            return
    try:
        #steps = oqread.FUNCTION(Qbfile)  # Should return a list with Add_step objects?
        print("Reading OpenQASM file is not implemented yet!")
        steps = [gf.Add_step(["PX", "CZnew"], [0, [0,1]], [np.pi, 0])]  # Temporary steps to not get syntax errors everywhere
    except:
        print(f"Couldn't read the OpenQASM file! Check that the filename, {OpenQASM}, is correct and that the file is "
              "constructed correctly. QnAS.solve() will now exit")
        return

    # Check n
    if n is None:
        """
        If n is none, we take the highest target as our number of qubits
        """
        maxi = -1
        print("You didn't specify the number of qubits. QnAS will use the number of qubits that are being targeted"
              " by the algorithm")
        for step in steps:
            for target in step.Tar_Con:
                if type(target) == int:
                    if target > maxi:
                        maxi = target
                elif type(target) == list:
                    if max(target) > maxi:
                        maxi = target
        if maxi == -1:
            print("No qubit has been targeted by the algorithm, number of qubits could not be decided."
                  " QnAS.solve() will now exit")
            return
        else:
            n = maxi + 1
    else:
        if not  1 <= n <= 15:
            print("Invalid value for n! Must be between 1 and 15! QnAS.solve() will now exit")
            return

    # Read qubit parameters
    if Qbfile is None:
        print("You didn't specify a file for the qubit parameters! \n"
              "QnAS assumes you have 3 levels, no noises and sets the anharmonicity to"
              " -225e6*2*pi for all qubits")
        Qblist = [qbc.Qubit(3, [0,0,0], -225e6 * 2 * np.pi, [i,i], [1,0,0]) for i in range(n)]
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
              " computer). If you leave it unspecified ntraj will automatically be 500. QnAS.solve() will now exit")
        return

    if tmax is None:
        print("No input for tmax! QnAS will use 1qb gate time: 20ns and 2qb gate time: 200ns!")
        tmax = [20e-9, 200e-9]

    if not type(tmax) == list:
        print("Invalid input for tmax! tmax must be a list of the form [1qb, 2qb] with "
              "max gate times for 1-qubit-gates and 2-qubit-gates given in seconds!"
              " QnAS.solve() will now exit")
        return
    if not 1e-12 < tmax[0] < 1e12 or 1e-12 < tmax[1] < 1e12:
        print("Invalid values for at least one of the max gate times. Limits are 1e-12 < t < 1e12. "
              " QnAS.solve() will now exit")
        return
    if type(store_time_dynamics) != bool:
        print("store_time_dynamics must be a boolean (True/False). "
              "QnAS.solve() will now exit")
        return

    psi0 = qbc.create_psi0(Qblist, 0)
    c_ops = co.create_c_ops(Qblist)

    args = {"steps" : steps, "c_ops" : c_ops, "psi0" : psi0, "Qblist": Qblist, "t_max": tmax, "ntraj" : ntraj, "StoreTimeDynamics": store_time_dynamics}
    return ma.main_algorithm(args)


if __name__ == "__main__":
    help()
