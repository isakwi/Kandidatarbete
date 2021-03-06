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
          "\"iSWAP\" iSWAP gate - Available in the iSWAP DLC, coming soon!\n"
          "Make sure these are the only gates you have included in your circuit to create the algorithm!\n"
          "\nDescription of functions: \n\n"
          "help()\n"
          "\t:You already called this function so you probably know that "
          "it just helps you get started!\n\n"
          "solve(Qbfile, circuit, zz_int, ntraj, tmax, store_time_dynamics, e_ops)\n"
          "\t:param Qbfile: Filepath that holds qubit parameters. Default - 3 levels, No noises, anharmonicity -225e6*2*pi [optional]\n"
          "\t:param circuit: Filepath that specifies circuit file.\n"
          "\t:param zz_int: symmetrical square (n x n) matrix that describes interaction between qubits. [optional]\n"
          "\t:param ntraj: number of trajectories for the Monte Carlo solver. Default - 500 [optional]\n"
          "\t:param tmax: Max time for 1qb-gate and 2qb-gate ~ [t_1qb, t_2qb]. Default - [20e-9, 200e-9] [optional]\n"
          "\t:param storeTimeDynamics: True/False value to store time dynamics. Default - False [optional]\n"
          "\t:param e_ops: Expectation value operators for storeTimeDynamics. Given as [[e_op1, Tar_Con],[e_op2, Tar_Con], ...] [optional]\n"
          "\t:return: if storeTimeDynamics is True: Returns ntraj many final states and two lists with exp values "
          "and corresponding times. Else: ntraj many final states\n\n"
          "The qubit parameter file needs to be located in the folder where you are running your program.\n"
          "Here is an example qubit file structure for 3 qubits (OBS! .csv file!):\n"
          "If you want more qubits, just add similar rows to the file!\n\n"
          "\tQubit;Relaxation(MHz);Dephasing(MHz);Thermal(MHz);Anharmonicity(MHz);Levels\n"
          "\t01;1.1;1.2;0.00;-229;3\n"
          "\t02;1.3;1.0;0.00;-225;3\n"
          "\t03;1.2;1.4;0.00;-226;3\n\n"
          "Here comes an example of how you can use qnas.solve() to solve a very simple system of 3\n"
          "qubits given that you have a qubit parameter file called 'qubitData.csv':\n\n"
          "\timport qnas\n"
          "\timport qiskit\n"
          "\tfrom numpy import pi\n"
          "\tcircuit = qiskit.QuantumCircuit(3)\n"
          "\tcircuit.rx(pi,0)\n"
          "\tcircuit.rx(pi,1)\n"
          "\tcircuit.rx(pi,2)\n"
          "\tfinalStates = qnas.solve(Qbfile='qubitData.csv', circuit=circuit)\n\n"
          "If you want descriptions about other functions that you want to use,\n"
          "Go read in the source descriptions under the function definitions!\n"
          "https://github.com/isakwi/Kandidatarbete/tree/main/qnas\n\n")
