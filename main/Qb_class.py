"""
Definition of Qubit object class
Should include
- Noise values
- Specified number
- beta? Qblvl ? initial state?
"""


import numpy as np
from qutip import *


'''Class for initiating Qubits, takes in following parameters:
 Beta= driving frequency
 level= number of energy levels for qubit
 noisert_vec = vector of rates of noises, 
 noisert_vec = [decoherence rate, dephasing rate, thermal noise rate]
 anharmonicity = anharmonicity frequency U in rad/s 
 desig = [x,y] is the spacial coordinate of the qubits on the chip given as coordinates in a plane, will be used to
 calculate if cubits can interact with each other
 init_cvec = array of coefficients for the initial state (first index represents coefficient for state |00...>) 
 notice that len(init_cvec) = level is required'''

class Qubit:

    def __init__(self, level, noisert_vec, anharm, desig, init_cvec):
        self.level = level
        self.noisert_vec = noisert_vec
        self.anharm = anharm
        self.desig = desig
        self.init_cvec = init_cvec
#function that calculates normalized initial state of qubit from init_cvec
    def initstate(self):
        norm = 0
        init_statemed = 0
        for i in range(0, len(self.init_cvec)):
            norm = norm + self.init_cvec[i] * np.conj(self.init_cvec[i])
            print(norm)


        for i in range(0, len(self.init_cvec)):
            init_statemed = init_statemed + (self.init_cvec[i] / (np.sqrt(norm))) * basis(self.level, i)

        init_state = init_statemed

        return init_state

def create_psi0(Qblist):
    """ If the initial states are always 0 for all qubits it might be easier
        to not have it in the Qubit-class and just have something like this!
        Can be added to another file to keep things in "main" nice and tidy!

            Creates initial state with all qubits in state 0: """
    psi0 = [basis(Qb.level, 0) for Qb in Qblist]
    return tensor(psi0)

