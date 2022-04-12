import qiskit
import re

qc = qiskit.QuantumCircuit.from_qasm_file('bench1.qasm')
qc.remove_final_measurements()

print(qc.draw())


gatelst = []
for i in range(qc.depth()):
    dag = qiskit.converters.circuit_to_dag(qc)
    layers = list(dag.multigraph_layers())
    # print(layers)
    n_remove = qc.depth() - i

    # the extra minus 1 since the last layer consists of output nodes (qubits and clbits).
    for layer in layers[- n_remove:]:

        for node in layer:
            if node.type == 'op':
                dag.remove_op_node(node)

    new_qc = qiskit.converters.dag_to_circuit(dag)
    gatelst.append(new_qc.qasm())

newgatelist = []  # function for splitting lines in gatelist. gatelist[n][k] gives nth depth, and kth element
for i in range(qc.depth()):
    newgatelist.append(gatelst[i].split('\n'))

    del newgatelist[i][0]
    del newgatelist[i][0]
    del newgatelist[i][0]
    if len(qc.clbits) != 0:
        del newgatelist[i][0]
    del newgatelist[i][-1]

for k in range(qc.depth()-1):
    for i in range(len(newgatelist[qc.depth() - 2 - k])):  # näst sista element, jobba sig neråt
        x = newgatelist[qc.depth() - 2 - k][i]  # näst sista listan, jobba sig neråt, i
        for j in range(len(newgatelist[qc.depth() - 1 - k])):
            if x == newgatelist[qc.depth() - 1 - k][j]:
                del newgatelist[qc.depth() - 1 - k][j]
                break

#print(newgatelist)

#ny del av program. parser


a =newgatelist

biggates = []
bigargs = []
bigqubits = []
for k in range(len(a)):
    #find gatetype
    gates = []
    for i in range(len(a[k])):
        if a[k][i].__contains__('('):
            ind = a[k][i].index('(')
            gates.append(a[k][i][0:ind])
        else:
            ind = a[k][i].index('q')
            gates.append(a[k][i][0:ind-1])

    #print(gates)

    #find argument
    args = []
    for i in range(len(a[k])):
        if "(" in a[k][i]:
            args.append(a[k][i][a[k][i].find("(")+1:a[k][i].find(")")]) # find thing inside parenthesis, if no parenthesis current prints entire thing
        else:
            args.append(0)
    #print(args)

    qubits = []
    for i in range(len(a[k])):
        lastbit = a[k][i][-3:-2]
        result = (re.search(r"\[([A-Za-z0-9_]+)\]", a[k][i]))
        if result.group(1) == lastbit:
            qubits.append(lastbit)
        else:
            qubits.append([result.group(1), lastbit])


    #print(qubits)
    biggates.append(gates)
    bigargs.append(args)
    bigqubits.append(qubits)

for i in range(qc.depth()):
    for j in range(len(biggates[i])):
        if biggates[i][j] == "cz":
            biggates[i][j] = "CZnew"
        if biggates[i][j] == "ry":
            biggates[i][j] = "PY"
        if biggates[i][j] == "rx":
            biggates[i][j] = "PX"
        if biggates[i][j] == "h":
            biggates[i][j] = '"HD"'
        if biggates[i][j] == "iswap":
            biggates[i][j] = "iSWAP"
        if biggates[i][j] == "pz":
            biggates[i][j] = "VPZ"
        #else:
        #    print("Gate " + biggates[i][j] + "not in library of qnas. ")

#for i in range(qc.depth()):
#    print(biggates[i])
#    print(bigargs[i])
#    print(bigqubits[i])

toqnas = []
for i in range(qc.depth()):
    for j in range(qc.depth()):
        toqnas.append([biggates[j], bigqubits[j], bigargs[j]])


print(toqnas)

for i in range(qc.depth()):
    print(toqnas[i])




#print(toqnas)





