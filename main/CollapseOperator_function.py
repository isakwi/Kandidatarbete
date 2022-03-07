import numpy as np
from qutip import *
import Qubitclass as qc

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

        for q in enumerate(qb_vec):


            if 0 < np.sqrt((q[1].desig[0] - qb[1].desig[0])**2 + (q[1].desig[1] - qb[1].desig[1])**2) < 1.0 and qb[1].noisert_vec[2] :
                eye_vec[qb[0]] = (destroy(qb[1].level).dag() * destroy(qb[1].level))
                eye_vec2[q[0]] = (destroy(q[1].level).dag() * destroy(q[1].level))

                cops_vec.append(np.sqrt((qb[1].noisert_vec[2] + q[1].noisert_vec[2])/2) * (tensor(eye_vec) * tensor(eye_vec2) + tensor(eye_vec2) * tensor(eye_vec)))


    return cops_vec

