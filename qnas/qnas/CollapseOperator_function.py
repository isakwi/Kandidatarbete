import numpy as np
from qutip import *
import math
from . import GateLib as gl

'''Takes array of instances of qubits from the Qubitclass as input, i need to add thermal noise and noise from unwanted 
interactions, unwanted interactions is alot trickier because we need to check if qubits can affect each other '''

#should add other gates like thermal noise

def Collapse_ops(qb_vec):
    cops_vec = []   #list for collapse operators
    eye_vec = []
    eye_vec2 = []

    for QB in enumerate(qb_vec):
        eye_vec.append(qeye(QB[1].level)) #array of identity matrices of correct dimensions
        eye_vec2.append(qeye(QB[1].level))


    for qb in enumerate(qb_vec):

        if qb[1].noisert_vec[0] > 0.0: #creating decoherence collapse operator
            eye_vec[qb[0]] = destroy(qb[1].level)
            cops_vec.append(np.sqrt(qb[1].noisert_vec[0]) * tensor(eye_vec))

        if qb[1].noisert_vec[1] > 0.0: #creating dephasing collapse operator
            eye_vec[qb[0]] = destroy(qb[1].level) * destroy(qb[1].level).dag()
            cops_vec.append(np.sqrt(qb[1].noisert_vec[1]) * tensor(eye_vec))
    return cops_vec


def create_c_ops(Qblist):
    """Alternative, maybe more compact? Makes use of the gatelib. But still need
    to add functionality for interaction (ZZ_interaction) and thermal excitation
    Returns a list with Qobj collapse operators"""
    c_ops = []
    for i in range(0, len(Qblist)):
        if Qblist[i].noisert_vec[0] > 0.0:  # Relaxation/Decoherence
            c_ops.append(math.sqrt(Qblist[i].noisert_vec[0]) * gl.PM(Qblist, i))
        if Qblist[i].noisert_vec[1] > 0.0:  # Dephasing
            c_ops.append(math.sqrt(Qblist[i].noisert_vec[1]) * gl.PZ(Qblist, i)/2)
        #if Qblist[i].noisert_vec[2] > 0.0:  # Thermal
            #c_ops.append(math.sqrt(Qblist[i].noisert_vec[3]) * gl.PM(Qblist, i).dag())  # Not sure about the thermal rates
    return c_ops
