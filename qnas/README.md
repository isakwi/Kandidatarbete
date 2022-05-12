Welcome to QnAS - an open source 
program to simulate noisy quantum algorithms!

Installation guide: Go to PyPI and find QnAS, 
there you can find the installation command! 
Or you can find it here:

    pip install qnas

MIT License: Free to use!

To see source code, go to: https://github.com/isakwi/Kandidatarbete/tree/main/qnas

To get started with QnAS, import QnAS to your
program and call the help function:

    import qnas

    qnas.help()

To get even more help, here comes an example 
of how you can use qnas.solve() to solve 
a very simple system of 3 qubits given that you 
have a qubit parameter file called 
'qubitData.csv':

    import qnas
    import qiskit
    from numpy import pi

    circuit = qiskit.QuantumCircuit(3)
    circuit.rx(pi,0)
    circuit.rx(pi,1)
    circuit.rx(pi,2)

    finalStates = qnas.solve(Qbfile='qubitData.csv', circuit=circuit)


