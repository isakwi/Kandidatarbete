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
          "Make sure these are the only gates you have included in your circuit to create the algorithm!\n"
          "\nDescription of functions: \n\n"
          "help()\n"
          "\t:You already called this function so you probably know that "
          "it just helps you get started!\n\n"
          "solve(Qbfile, circuit, n, ntraj, tmax, store_time_dynamics)\n"
          "\t:param Qbfile: Filepath that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi\n"
          "\t:param circuit: Filepath that specifies circuit file. Default - Asks user to specify gates manually or not run\n"
          "\t:param zz_int: 15x15 matrix that describes interaction between qubits.\n"
          "\t:param ntraj: number of trajectories for the Monte Carlo solver. Default - 500\n"
          "\t:param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9]\n"
          "\t:param store_time_dynamics: True/False value to store time dynamics. Default - False\n"
          "\t:param e_ops: Expectation value operators for store_time_dynamics. Given as [[e_op1, Tar_Con],[e_op2, Tar_Con], ...]\n"
          "\t:return: if store_time_dynamics is True: Returns ntraj many final states and two lists with exp values "
          "and corresponding times. Else: ntraj many final states\n\n"
          "The qubit parameter file needs to be located in the folder where you are running your program.\n"
          "Here is an example qubit file structure (OBS! .csv file!):\n"
          "\tQubit;Relaxation;Dephasing;Thermal;Anharmonicity(MHz);Levels\n"
          "\t01;0.00;0.00;0.00;-229;3\n"
          "\t02;0.01;0.00;0.00;-225;3\n"
          "\t03;0.01;0.00;0.00;200;3\n"
          "\t04;0.04;0.00;0.00;200;3\n"
          "\t05;0.05;0.00;0.00;200;2\n"
          "\t06;0.06;0.00;0.00;200;2\n"
          "\t07;0.07;0.00;0.00;200;2\n"
          "\t08;0.08;0.00;0.00;200;2\n"
          "\t09;0.09;0.00;0.00;200;2\n"
          "\t10;0.10;0.00;0.00;200;2\n"
          "\t11;0.11;0.00;0.00;200;2\n"
          "\t12;0.12;0.00;0.00;200;2\n"
          "\t13;0.02;0.00;0.00;200;2\n"
          "\t14;0.02;0.00;0.00;200;2\n"
          "\t15;0.02;0.00;0.00;200;2\n\n"
          "Do you want to donate to QnAS development to keep the project going forward?\n"
          "Swish to +46 70 603 61 27, thanks!")
