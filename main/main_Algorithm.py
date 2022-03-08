from qutip import *
import numpy as np
#TODO: replace everything until the for loop and
## This script doesn't need to explicitly know the number of qubits
##Assume that we have a steps[] data set
## Also assume that the gates are implemented iin the Hamiltonian
a = destroy(2)
pi = np.pi
beta = 4*pi/2e-9
inputfile = {"steps" : [{"gate": a.dag() * a}], "psi0": (basis(2,0)+basis(2,1))/np.sqrt(2), "c_ops" : [np.sqrt(0.1) * a], "tlists" : [np.linspace(0,2e-9,101)], "virtualgates" : [None], "e_ops" : [a.dag() * a]}
psi0 = []
steps = inputfile["steps"]
psi0.append(inputfile["psi0"]) #initial state before the algorithm is run
c_ops = inputfile["c_ops"]
tlists = inputfile["tlists"]
e_ops = inputfile["e_ops"]
virtualgates = inputfile["virtualgates"] #rotations around the z axis

##--------EVERYTHING ABOVE THIS IS JUST TAKING IN INPUT
for i in range(len(steps)):
    H = beta/2 * steps[i]["gate"]
    output = mcsolve(H,psi0[i], tlists[i],  c_ops= c_ops, ntraj = 1)
    currentstate = output.states
    #the virtual gates should be able to apply through matrix multiplication
    if virtualgates[i] != None:
        currentstate = virtualgates[i] * currentstate
    psi0.append(currentstate)
    print(psi0[-1])

