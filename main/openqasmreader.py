import numpy as np

from qutip import *
import qiskit
import gateLib as gl
import gateFuncs as gf

"""basic initial idea: take in qasmfile and convert the steps to a array of strings [gate1 q[n],...,] and then extract
an array that contains the order of gates being applied to qubits, use this array to determine which gates should 
be in the same level when adding them as steps."""


circuit = qiskit.QuantumCircuit(3)
circuit.h(1)
circuit.h(0)
circuit.h(0)
circuit.h(1)
#circuit.cx(0, 1)
#circuit.h(1)
#circuit.cx(1, 0)
#circuit.h(2)
#circuit.cx(2, 1)
#circuit.h(0)
#circuit.h(1)
#circuit.h(0)


"""creates text file from openqasm circuit"""
def create_file(circ):
    file = circ.qasm(formatted=True, filename='circfile.txt')

    return file


"""takes in openqasm circuit and returns array cointaining the gates in order and what qubits  
they are applied on"""

def get_arr(circ):

    file = create_file(circuit)
    with open('circfile.txt', 'r') as tx:
        str_arr = tx.readlines()
    arr = np.array(str_arr)

    return arr

array = get_arr(circuit)

"""splits string in to array of its charachters"""
def split_char(word):
    return [char for char in word]

"""function that takes in array of strings (generated from openqasm file),
and returns array of the order of wich qubits gets a gate applied on it, can be used to determine 
what gates should be in each level when they are added as steps"""

def get_qb_order(arr):
    arrc = arr[3:]
    qo_arr = []

    for stp in enumerate(arrc):
        tar =[]
        charlist= split_char(stp[1])

        for word in charlist:

            if word.isdigit():

                tar.append(int(word))

        qo_arr.append(tar)
    return qo_arr

qovec = get_qb_order(array)

#print(qovec)

"""def what_gate(arr, step):
    arrc = arr[3:]
    frst_wrd = arrc[step].split()[0]
    qb_ord = get_qb_order(arr)

    for qb in enumerate(qb_ord):
        print(0)
"""

"""function that takes in array of strings and returns array of qubits in their levels in the circuit
"""

def order_level(arr):
    qb_ord = get_qb_order(arr)
    ol_arr=[]
    levelvec=[[]]
    totlen=0
    level=0
    for qub in enumerate(qb_ord):


        for el in enumerate(levelvec[0]):
            totlen = len(el[1]) + totlen
            #print(totlen)
            #print(levelvec)

        if totlen >= len(qb_ord):
            print('done')
            break

        if qub[0] == 0:
            #ol_arr.append(qub[1])
            slqb_arr = qb_ord[1:]
            #print(slqb_arr)
            print('here')

        elif qub[1] in levelvec[0][level-1] != True:   #levelvec[qub[0]-1]
            ol_arr.append(qub[1])

        #print(ol_arr)
        for tar in enumerate(qub[1]):

            if qub[0] == 0:
                ol_arr.append(qub[1])
                #slqb_arr = qb_ord[1:]
                # print(slqb_arr)

            #print(tar[1])
            for qb in enumerate(slqb_arr[qub[0]+1:]):
                exist = tar[1] in qb[1]
                #print(exist)
                #print(qb[1])



            """for el in enumerate(levelvec):
                totlen = len(el[1]) + totlen
                print(totlen)
                print(levelvec)

            if totlen >= len(qb_ord):
                break
"""
            if exist != True:       #append to ol_arr[level]
                ol_arr.append(qb[1])
                #print(qb[1])
            else:
                level = level + 1
                print(level)

        if qub[0] == 0:
            levelvec[0].append(ol_arr.copy())
        else:
            levelvec[0].append(ol_arr.copy())
        ol_arr.clear()
        totlen=0
    return levelvec[0]

#nivvec = order_level(array)

#print(nivvec)




def order_level2(array, depth):
    qb_ord = get_qb_order(array)
    ol_arr =[]
    levelvec = [[]] * depth  # each level is array containing array of targets
    totlen = 0
    level = -1

    for qub in enumerate(qb_ord):
        totlen = 0
        exist1 = False
        exist2 = False
        print('new it')



        for el in enumerate(levelvec):
            totlen = totlen + len(levelvec[el[0]])
        #print(totlen)

        if totlen >= len(qb_ord) : #or level +1>= depth
            print('done')
            break


        if qub[0] == 0:
            # ol_arr.append(qub[1])
            slqb_arr = qb_ord[1:]
            levelvec[0] =[qub[1]]
            print('living')

        if qub[0] != 0:
            #print(levelvec)
            print(level)

            for t in enumerate(qub[1]):
                print(levelvec)# test if gate should be applied in new level
                for p in enumerate(levelvec[level-1]):
                    if t[1] in p[1]:
                        print('A')
                        print(t[1])
                        print('B')
                        exist1 = True
        print(exist1)
        if exist1:
            print('bajs',qub[1])

            ol_arr =[qub[1]]
            #ol_arr.append(qub[1])
            print(ol_arr, qub[1])
            print('new level')
        print('nu')
        print(levelvec)
        print('du')
        #print(levelvec[level+1])
        print(level)
        for tar in enumerate(levelvec[level +1]): # var qub[1]  sen levelvec[level +1]
            exist2 = False
            print(tar[1])
            print('doing tar')

            print(qub[0])
            if qub[0] == 0:
                ol_arr.append(qub[1])
                print('pls stop')

                #slqb_arr = qb_ord[1:]
                # print(slqb_arr)
                #print(ol_arr)
                #print('here')

                for qb in enumerate(slqb_arr):  #var slqb_arr
                    print('here A')
                    print(qb[1])
                    print(tar[1])
                    for elt in enumerate(qb[1]):
                        print('korpa')
                        if elt[1] in tar[1]: #var tar[1] in qb[1]
                            exist2 = True
                        for pr in enumerate(ol_arr):
                            if elt[1] in pr[1]:
                                exist2 = True



                    if exist2 != True :  # append to ol_arr[level]
                        ol_arr.append(qb[1])
                        # print(qb[1])
                        print('appended to level')
                    else:
                        level = level + 1
                        print('already existed, new level A')
                        # print(level)

                        levelvec[level] = (ol_arr.copy())
                        #levelvec[level+1] = [qb[1]]
                        ol_arr = [qb[1]]
                        levelvec[level + 1] = ol_arr

                        #print('appended')
                        print(levelvec)

                        break


            else:
                print('nu vi har')
                print(ol_arr)
                print(levelvec)
                print(level+1)

                for qb in enumerate(ol_arr): #slqb_arr[qub[0]:] sen ol_arr
                    #print(ol_arr)
                    #print('here wtf')
                    #print(qb[1])
                    print(tar[1], qb[1])

                for elt in enumerate(qb[1]):
                    print('korpa')
                    if elt[1] in tar[1]:  # var tar[1] in qb[1]
                        exist2 = True
                    for pr in enumerate(ol_arr):
                        if elt[1] in pr[1]:
                            exist2 = True


                    if exist2 != True:       #append to ol_arr[level]
                        ol_arr.append(qb[1])
                        #print(qb[1])
                        #print('appended')
                    else:
                        level = level + 1
                        print('already existed in level B')
                        #print(level)
                        levelvec[level] = ol_arr.copy()
                        if level+1 < depth:
                            levelvec[level + 1] = [qb[1]]
                        print(levelvec)
                        print('dinmamma')
                        ol_arr.clear()
                        break
                else:
                    continue
                    print('kor')
                    levelvec[level]=(ol_arr.copy())
                print('stop')
                break

                    #levelvec.append(ol_arr.copy())
                    #ol_arr.clear()


    return levelvec


nivvec2 = order_level2(array, circuit.depth())

print(nivvec2)

circuit.depth()




