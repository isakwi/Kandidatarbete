__all__ = ['qasmToQnas']

from qiskit.converters import circuit_to_dag, dag_to_circuit
from re import search
from numpy import pi
from . import gateFuncs as gf


def qasmToQnas(circuit):
    """
    Translates qiskit circuits to QnAS circuit.
    Input:
    - OpenQASM quantum circuit (qiskit QuantumCircuit object)
    - show_circuit = option to print circuit, optional
    Output: list of AlgStep objects for the algorithm.
    """
    qc = circuit
    qc.remove_final_measurements()  # Removing final measure

    def piDelivery(s):  # takes in string s and returns float of string
        """
        Translates strings to float
        Input:
        - string
        Output: float
        """
        flt = 0
        if '*pi/' in s:
            flt = float(s.split('*')[0]) * pi / float(s.split('/')[1])
        elif '*pi' in s:
            flt = float(s.split('*')[0]) * pi
        elif '-pi/' in s:
            flt = -pi / float(s.split('/')[1])
        elif 'pi/' in s:
            flt = pi / float(s.split('/')[1])
        elif '-pi' in s:
            flt = -pi
        elif 'pi' in s:
            flt = pi
        else:
            flt = float(s)
        return flt

    gatelist = []
    for i in range(qc.depth()):  # splits circuit into steps
        dag = circuit_to_dag(qc)
        layers = list(dag.multigraph_layers())
        n_remove = qc.depth() - i

        # the extra minus 1 since the last layer consists of output nodes (qubits and clbits).
        for layer in layers[- n_remove:]:

            for node in layer:
                if node.type == 'op':
                    dag.remove_op_node(node)


        new_qc = dag_to_circuit(dag)
        gatelist.append(new_qc.qasm())

    newgatelist = []  # function for splitting lines in gatelist. gatelist[n][k] gives nth depth, and kth element
    for i in range(qc.depth()):
        newgatelist.append(gatelist[i].split('\n'))
        del newgatelist[i][0]
        del newgatelist[i][0]
        del newgatelist[i][0]
        if len(qc.clbits) != 0:
            del newgatelist[i][
                0]  # deletes the first three or four lines of the qasm file which contain the filetype, ammount of qubits etc..
        del newgatelist[i][-1]

    for k in range(qc.depth() - 1):
        for i in range(len(newgatelist[qc.depth() - 2 - k])):  # näst sista element i lista, jobba sig neråt
            x = newgatelist[qc.depth() - 2 - k][i]  # näst sista listan, jobba sig neråt
            for j in range(len(newgatelist[qc.depth() - 1 - k])):
                if x == newgatelist[qc.depth() - 1 - k][j]:
                    del newgatelist[qc.depth() - 1 - k][j]
                    break

    a = newgatelist

    allgates = []  # lists that will contain the gates
    allargs = []
    allqubits = []

    for k in range(len(a)):
        # find gatetype by reading everything until a "(" or "q" is detected
        gates = []
        for i in range(len(a[k])):
            if a[k][i].__contains__('('):
                ind = a[k][i].index('(')
                gates.append(a[k][i][0:ind])
            else:
                ind = a[k][i].index('q')
                gates.append(a[k][i][0:ind - 1])

        # find argument by reading whatever is inside of the parenthesis
        args = []
        for i in range(len(a[k])):
            if "(" in a[k][i]:
                args.append(piDelivery(a[k][i][a[k][i].find("(") + 1:a[k][i].find(
                    ")")]))  # find item inside parenthesis, if no parenthesis current append 0
            else:
                args.append(0)

        # find which qubits are acted on in each step by finding reading what's inside the "[]". If it's a two qubit gate both are added
        qubits = []
        for i in range(len(a[k])):
            lastbit = a[k][i][-3:-2]
            if a[k][i][-4:-2].isdigit():
                lastbit = a[k][i][-4:-2]
            result = (search(r"\[([A-Za-z0-9_]+)\]", a[k][i]))
            if result.group(1) == lastbit:
                qubits.append(int(lastbit))
            else:
                qubits.append([int(result.group(1)), int(lastbit)])

        allgates.append(gates)
        allargs.append(args)
        allqubits.append(qubits)

    for i in range(qc.depth()):
        for j in range(len(allgates[i])):
            if allgates[i][j] == "cz":
                allgates[i][j] = "CZ"
            if allgates[i][j] == "ry":
                allgates[i][j] = "PY"
            if allgates[i][j] == "rx":
                allgates[i][j] = "PX"
            if allgates[i][j] == "h":
                allgates[i][j] = "HD"
            if allgates[i][j] == "iswap":
                allgates[i][j] = "iSWAP"
            if allgates[i][j] == "rz":
                allgates[i][j] = "VPZ"
            if allgates[i][j] == "id":
                allgates[i][j] = "ID"

    toqnas = []
    for j in range(qc.depth()):
        toqnas.append([allgates[j], allqubits[j], allargs[j]])

    steps = []
    for stp in enumerate(toqnas):
        steps.append(gf.AlgStep(stp[1][0], stp[1][1], stp[1][2]))
    return steps
