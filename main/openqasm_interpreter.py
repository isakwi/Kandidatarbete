import qiskit
import re
import numpy as np
import GateFuncs as gf


def qasm_to_qnas(circuit):
    qc = circuit
    qc.remove_final_measurements()  # Removing final measure

    show_circuit = False  # you wish to see the circuit and how it's arguments are updated
    if show_circuit:
        print(qc)
        # qc.draw(output='mpl')
        # plt.show()

    def pi_delivery(s):  # takes in string s and returns float of string
        flt = 0
        if '*pi/' in s:
            flt = float(s.split('*')[0]) * np.pi / float(s.split('/')[1])
        elif '*pi' in s:
            flt = float(s.split('*')[0]) * np.pi
        elif 'pi/' in s:
            flt = np.pi / float(s.split('/')[1])
        elif 'pi' in s:
            flt = np.pi
        else:
            flt = float(s)
        return flt

    gatelist = []
    for i in range(qc.depth()):  # splits circuit into steps
        dag = qiskit.converters.circuit_to_dag(qc)
        layers = list(dag.multigraph_layers())
        n_remove = qc.depth() - i

        # the extra minus 1 since the last layer consists of output nodes (qubits and clbits).
        for layer in layers[- n_remove:]:

            for node in layer:
                if node.type == 'op':
                    dag.remove_op_node(node)

        new_qc = qiskit.converters.dag_to_circuit(dag)
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

    # ny del av program. parser

    a = newgatelist

    allgates = []  # lists that will contain the
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
                args.append(pi_delivery(a[k][i][a[k][i].find("(") + 1:a[k][i].find(
                    ")")]))  # find item inside parenthesis, if no parenthesis current append 0
            else:
                args.append(0)

        # find which qubits are acted on in each step by finding reading what's inside the "[]". If it's a two qubit gate both are added
        qubits = []
        for i in range(len(a[k])):
            lastbit = a[k][i][-3:-2]
            result = (re.search(r"\[([A-Za-z0-9_]+)\]", a[k][i]))
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
                allgates[i][j] = "CZnew"
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
        steps.append(gf.Add_step(stp[1][0], stp[1][1], stp[1][2]))
    return steps


def num_qubits(qc): #useless function for getting number of qubits from circuit. Use qc.num_qubits instead
    return qc.num_qubits


"""qc = qiskit.QuantumCircuit.from_qasm_file('bench2.qasm')  # For testing the file from here
steve = qasm_to_qnas(qc)
print(steve)""" #retrun "toqnas" if you wish to see QnAS style of adding gates.
