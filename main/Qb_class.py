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
 noisert_vec = [decoherence rate, dephasing rate, interaction rate, thermal noise rate]
 desig = [x,y] is the spacial coordinate of the qubits on the chip given as coordinates in a plane, will be used to
 calculate if cubits can interact with each other
 init_cvec = array of coefficients for the initial state (first index represents coefficient for state |00...>) 
 notice that len(init_cvec) = level is required'''

class Qubit:

    def __init__(self, level, noisert_vec, desig, init_cvec):
        self.level = level
        self.noisert_vec = noisert_vec
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

