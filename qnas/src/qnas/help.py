__all__ = ['help']

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
          "\t:You already called this function so you probably know that "
          "it just helps you get started!\n\n"
          "solve(Qbfile, OpenQASM, n, ntraj, tmax, store_time_dynamics)\n"
          "\t:param Qbfile: Filepath that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi\n"
          "\t:param OpenQASM: Filepath that specifies OpenQASM file. Default - Asks user to specify gates manually or not run\n"
          "\t:param int_matrix: 15x15 matrix that describes interaction between qubits."
          "\t:param ntraj: number of trajectories for the Monte Carlo solver. Default - 500\n"
          "\t:param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9]\n"
          "\t:param store_time_dynamics: True/False value to store time dynamics. Default - False\n"
          "\t:return: if store_time_dynamics is True: Not sure yet. Else: ntraj many final states\n\n"
          "Do you want to donate to QnAS development to keep the project going forward?\n"
          "Swish to +46 70 603 61 27, thanks!")
