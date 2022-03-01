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
# Hej
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from IPython.display import Image
from qutip import *
from qutip.measurement import measure, measurement_statistics


w_01 = 4*1e9 *2*np.pi   # Qubit frequency (4-5 GHz)
w_d = w_01
U = 200*1e6 *2*np.pi   # Anhormicity (only if levels > 2 ) (150-250 MHz)

t_1q = 20*1e-9   #1qubit gate time 
t_2q = 200*1e-9  #2qubit gate time 


"""
INPUTS: 
    Choose Number of qubits (up to 8)
    Choose drive angle and drive start for each qubit
    
"""

MaxNoOfQubits = 8  
NoOfQubits = 8 # Choose how many qubits you want to run No more than 8
inputs = [[np.pi, t_1q, 10*1e-9],   # [drive angle0, drive time 0, drive start 0],
          [np.pi/4,t_1q, 0     ],   # [drive angle1...] 
          [np.pi/2,t_1q, 4*1e-8],
          [np.pi/8,t_1q, 0     ],
          [np.pi/3,t_1q, 0     ],
          [np.pi/16,t_1q, 0    ],
          [np.pi/5,t_1q, 0    ],
          [np.pi*2,t_1q, 0     ]]

Qubitstates0 =np.zeros(NoOfQubits) #Initial state of qubits (all = 0), change as you please


T1 = 50*1e-6 # relax time
Tphi = 100*1e-6 # dephase time 
relax_rate =(1/T1)*np.ones(NoOfQubits) #Same rates for everythin, change if u want
dephas_rate = (1/Tphi)*np.ones(NoOfQubits) #Same rates for everythin, change if u want

use_MCWF = True
ntraj = 10


#%%

tlist=np.linspace(0,1*1e-7,101)

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
gate=DimensionifyOperator((a+a.dag()), NoOfQubits, np.ones(NoOfQubits))


#Anharmonicity 
H_anh  = 0
H_anhh = DimensionifyOperator(U*a.dag()*a.dag()*a*a, NoOfQubits, np.ones(NoOfQubits))
for i in range(NoOfQubits):
    H_anh = H_anh + H_anhh[i]

#%%Timefuncs
def EnvelopeFunc (t, beta, t_qd, t_st):
    # Models the drive pulse as E(t) = A*cos^2(tπ/t_qd - π/2), 
    # Used in the time functions Et# which are used in H = QobjEvo 
    A    = beta/t_qd
    E = A*np.cos((t-t_st)*np.pi/t_qd-np.pi/2)**2
    if t_st<t<t_qd+t_st:
         return E
    else: 
        return 0

def Et0 (t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et0'][0] #Drive angle 
    t_qd = args['Et0'][1] #Gate time 
    t_st = args['Et0'][2] #Start time for drive 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et1(t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et1'][0] #Drive angle 
    t_qd = args['Et1'][1] #Gate time 
    t_st = args['Et1'][2] #Start time 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et2 (t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et2'][0] #Drive angle 
    t_qd = args['Et2'][1] #Gate time 
    t_st = args['Et2'][2] #Start time for drive 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et3(t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et3'][0] #Drive angle 
    t_qd = args['Et3'][1] #Gate time 
    t_st = args['Et3'][2] #Start time 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et4 (t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et4'][0] #Drive angle 
    t_qd = args['Et4'][1] #Gate time 
    t_st = args['Et4'][2] #Start time for drive 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et5(t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et5'][0] #Drive angle 
    t_qd = args['Et5'][1] #Gate time 
    t_st = args['Et5'][2] #Start time 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et6 (t, args):
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et6'][0] #Drive angle 
    t_qd = args['Et6'][1] #Gate time 
    t_st = args['Et6'][2] #Start time for drive 
    return EnvelopeFunc(t, beta, t_qd, t_st)

def Et7(t, args): 
    # args in form {'beta': value, 't_qd': value}
    beta = args['Et7'][0] #Drive angle 
    t_qd = args['Et7'][1] #Gate time 
    t_st = args['Et7'][2] #Start time 
    return EnvelopeFunc(t, beta, t_qd, t_st)

#%% Time dependance of H 
inp={'Et0': inputs[0],'Et1': inputs[1],'Et2': inputs[2],'Et3': inputs[3],'Et4': inputs[4],'Et5': inputs[5],'Et6': inputs[6],'Et7': inputs[7]}
# 
if len(gate)==1:
    H = QobjEvo([H_anh,[gate[0],Et0]],args=inp)
elif len(gate)==2:
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1]],args=inp)
elif len(gate)==3:
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1],[gate[2], Et2]],args=inp)
elif len(gate)==4:
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1],[gate[2], Et2],[gate[3], Et3]],args=inp)
elif len(gate)==5:
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1],[gate[2], Et2],[gate[3], Et3],[gate[4], Et4]],args=inp)
elif len(gate)==6: 
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1],[gate[2], Et2],[gate[3], Et3],[gate[4], Et4],[gate[5], Et5]],args=inp)
elif len(gate)==7:
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1],[gate[2], Et2],[gate[3], Et3],[gate[4], Et4],[gate[5], Et5],[gate[6], Et6]],args=inp)
elif len(gate)==8:
    H = QobjEvo([H_anh,[gate[0],Et0],[gate[1], Et1],[gate[2], Et2],[gate[3], Et3],[gate[4], Et4],[gate[5], Et5],[gate[6], Et6],[gate[7], Et7]],args=inp)
    


#%% Expectations and collapse operators 

e_ops=DimensionifyOperator(a.dag()*a, NoOfQubits, np.ones(MaxNoOfQubits))

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
    fig1.plot(tlist, result.expect[i], label='Qb'+str(i+1)+ '~ drive: '+ str(round((inputs[i][0]/np.pi),3)) +' π')
fig1.set_ylabel('Ockupation prob')
fig1.set_xlabel('t')
fig1.grid()
fig1.legend(loc='upper right')
fig1.axis([0,tlist[-1],0,2.05])
fig1.title.set_text('Qubit states')

for i in range(NoOfQubits):
    drive=[]
    for t in tlist:
        drive.append(Et0(t,{'Et0': inputs[i]})) 
    fig2.plot(tlist, drive, label='Envelope #'+str(i+1)+ ' ~'+ str(round((inputs[i][0]/np.pi),3)) +' π' )

fig2.set_ylabel('E(t)')
fig2.set_xlabel('t')
fig2.grid()
fig2.legend()
fig2.title.set_text('Drive Envelopes')

