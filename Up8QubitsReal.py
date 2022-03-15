#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 10:53:03 2022

@author: edvinmartinson


Simulating Qubits  with REAL VALUES 

H_qubits = ∑_i w*a_i.dag()*a_i + U * a_i.dag()*a_i.dag()*a_i*a_i + H_i_drive

H_i_drive = b cos(w_d t) (a_i + a_i.dag())

Incorporate drive pulse E(t) = Acos^2(t),  

"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from IPython.display import Image
from qutip import *
from qutip.measurement import measure, measurement_statistics


w_01 = 4*1e9 *2*np.pi   # Qubit frequency (4-5 GHz)
w_d = w_01
U = -200*1e6 *2*np.pi   # Anhormicity (only if levels > 2 ) (150-250 MHz)

t_1q = 20*1e-9   #1qubit gate time 
t_2q =200*1e-9  #2qubit gate time 


"""
INPUTS: 
    Choose Number of qubits (up to 8)
    Choose drive angle and drive start for each qubit
    
"""

MaxNoOfQubits = 8  
NoOfQubits = 2 # Choose how many qubits you want to run No more than 8
inputs = [[np.pi*2, t_2q, 0* 10*1e-9],   # [drive angle0, maxgate time 0, drive start 0],
          [np.pi/2*0,t_2q, 0     ],   # [drive angle1...] 
          [np.pi/3,t_1q, 4*1e-8],
          [np.pi/4,t_1q, 2*1e-8],
          [np.pi/5,t_1q, 0     ],
          [np.pi/6,t_1q, 0     ],
          [np.pi/7,t_1q, 0     ],
          [np.pi*2,t_1q, 0     ]]

Qubitstates0 =np.ones(NoOfQubits) #Initial state of qubits (all = 0), change as you please


T1 = 50*1e-6 # relax time
Tphi = 100*1e-6 # dephase time 
relax_rate =(1/T1)*np.ones(NoOfQubits) #Same rates for everythin, change if u want
dephas_rate = (1/Tphi)*np.ones(NoOfQubits) #Same rates for everythin, change if u want

use_MCWF = True
ntraj = 10


#%%

tlist=np.linspace(0,6*1e-7,101)

psi0 = basis(3,int(Qubitstates0[0]))
for j in range(NoOfQubits-1):
    psi0 = tensor(psi0, basis(3,int(Qubitstates0[j+1])))

a=destroy(3)

def DimensionifyOperator(Q, NoOfQubits, vals):
    #Create list of operators that could act on each qubit. 
    # That is gate[0] => operate on qubit1, gate[3] => operate on qubit4.. etc
    # Q = Operator, vals= array of length MaxNoOQubits with values s.a. rates for each qubit
    Opers = []
    Qlist = []
    for i in range(NoOfQubits):
        Qlist.append(qeye(3)) # Start with list of Identity-ops 
    for j in range(NoOfQubits):
        Qlist[j]=vals[j]*Q    # Change one at a time to Q-op and tensor 
        Opers.append(tensor(Qlist))
        Qlist[j]=qeye(3)      #Reset for next loop 
    return Opers
    
    
def TensorifyOperator(Q, NoOfQubits):
    #Tensorproduct for length NoOfQubits 
    # Q = Operator 
    Qlist = []
    for i in range(NoOfQubits):
        Qlist.append(Q)
    return tensor(Qlist)


# Create list of gates that could run on each qubit. That is gate[0] => operate on qubit1, gate[3] => operate on qubit4
#gate=DimensionifyOperator((a+a.dag()), NoOfQubits, np.ones(NoOfQubits))

gate=tensor(basis(3,1),basis(3,1))*tensor(basis(3,2),basis(3,0)).dag()+tensor(basis(3,2),basis(3,0))*tensor(basis(3,1),basis(3,1)).dag()

#Anharmonicity 
H_anh  = 0
H_anhh = DimensionifyOperator(U*a.dag()*a.dag()*a*a, NoOfQubits, np.ones(NoOfQubits))
for i in range(NoOfQubits):
    H_anh = H_anh + H_anhh[i]

#%%Timefuncs

# def EnvelopeFunc (t, beta, t_m, t_d, t_st): 
#     # Models the drive pulse as E(t) = A*cos^2(tπ/t_d - π/2), 
#     # Used in the time functions Et# which are used in H = QobjEvo 
#     # beta = drive strength
#     # t_m = t_max gate time (~ ang=π)
#     # t_d =drive time, 
#     # t_st = start time 
#     E    = beta/2*np.sin((t-t_st)*np.pi/t_d)**2
#     return E*np.heaviside(t_st+t_d-t,1)*np.heaviside(t-t_st,1)


# def TimeFunc (t, args): 
#     # To be called from QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)
#     # where inputs[i] is an array of dim3 with values for i:th qubit
#     ang  = args[0]  # Drive angle 
#     t_m  = args[1]  # Max gate time (~ ang=π)
#     t_st = args[2]  # Start time for drive 
#     beta = 2*np.pi/t_m    #Drive strength
#     t_d = t_m * ang/np.pi # Drive time for specified angle
#     return EnvelopeFunc(t, beta, t_m, t_d, t_st)

def EnvelopeFunc (t, beta, t_m, t_d, t_st): 
    # Models the drive pulse as E(t) = A*cos^2(tπ/t_d - π/2), 
    # Used in the time functions Et# which are used in H = QobjEvo 
    # beta = drive strength
    # t_m = t_max gate time (~ ang=π)
    # t_d =drive time, 
    # t_st = start time 
    E    = beta/2*np.sin((t-t_st)*np.pi/t_d)**2
    return E*np.heaviside(t_st+t_d-t,1)*np.heaviside(t-t_st,1)


def TimeFunc (t, args): 
    # To be called from QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)
    # where inputs[i] is an array of vals for i:th qubit
    ang  = args[0]  # Drive angle 
    t_m  = args[1]  # Max gate time (~ ang=π)
    t_st = args[2]  # Start time for drive 
    if t_m < 100*1e-9:   # Python makes t_max not quite 200ns for 2qb.
        beta = 2*np.pi/t_m    #Drive strength
        t_d = t_m * ang / np.pi  # Drive time for specified angle
    else:
        beta = 4*np.pi/t_m  #Drive strength should corespond to 2π drive angle for 2qb gates
        t_d = t_m *ang/(2*np.pi)
    return EnvelopeFunc(t, beta, t_m, t_d, t_st)





#%% Time dependance of H 

H = H_anh
#for i in range(len(gate)):
#    H= H + QobjEvo([gate[i],TimeFunc(tlist, inputs[i])], tlist=tlist)
H= H + QobjEvo([gate,TimeFunc(tlist, inputs[0])], tlist=tlist)

#%% Expectations and collapse operators 

hejhej=Qobj([[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,np.sqrt(2),0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]])
hejhejhej=Qobj([[0,0,0],
                [0,0,0],
                [0,0,2]])
print(hejhej)
hejh = tensor(Qobj([[0,0,0],
             [0,1,0],
             [0,0,0]]), qeye(3))
hhej=tensor(hejhejhej,qeye(3))+hejh

e_ops=hhej #DimensionifyOperator(a.dag()*a, NoOfQubits, np.ones(MaxNoOfQubits))

c_ops1 = DimensionifyOperator(a, NoOfQubits, np.sqrt(relax_rate))
c_ops2 = DimensionifyOperator(qeye(3), NoOfQubits, np.sqrt(dephas_rate))
#What is the dephasing operator in 3level?? 

c_ops=c_ops1+c_ops2


#%% Results 

if use_MCWF:
    result = mcsolve(H, psi0, tlist, c_ops, e_ops, ntraj)
else:
    result = mesolve(H, psi0, tlist, c_ops, e_ops)
#%%
fig, [fig1,fig2] = plt.subplots(2,1, sharex=True,figsize=(7,7))
for i in range(NoOfQubits):
    fig1.plot(tlist, result.expect[0], label='Qb'+str(i+1)+ '~ drive: '+ str(round((inputs[i][0]/np.pi),3)) +' π')
fig1.set_ylabel('Ockupation prob')
fig1.set_xlabel('t')
fig1.grid()
fig1.legend(loc='upper right')
fig1.axis([0,tlist[-1],0,2.05])
fig1.title.set_text('Qubit states')

for i in range(NoOfQubits):
    drive=[]
    for t in tlist:
        drive.append(TimeFunc(t,inputs[i])) 
    fig2.plot(tlist, drive, label='Envelope #'+str(i+1)+ ' ~'+ str(round((inputs[i][0]/np.pi),3)) +' π' )

fig2.set_ylabel('E(t)')
fig2.set_xlabel('t')
fig2.grid()
fig2.legend()
fig2.title.set_text('Drive Envelopes')

