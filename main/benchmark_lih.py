import numpy as np
import GateFuncs as gf
import CollapseOperator_function as colf
import main_Algorithm as ma
#import main_Alg_parfortest as ma  #Uncomment to change to parfor from the start
from qutip import *
import GateLib as gl
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import Qb_class as qbc
import matplotlib as mpl
import pandas as pd
from bayes_opt import BayesianOptimization


l = 3 #qubit energy level
"""The H defined immediately below is the cost function"""
sx = destroy(l) + create(l)
sy = -1j * (destroy(l) - create(l))
sz= 2 * create(l) * destroy(l) - qeye(l)
I = qeye(l)
df = pd.read_excel('LiH_cost_function_data.xlsx', header = 0)
ops = df["Operator"].values
weights = df["Weight"].values
opDict = {"I": I, "X": sx, "Y": sy, "Z": sz}
H = 0 #our cost function
for i in range(len(ops)):
    Hlist = []
    word = ops[i]
    for letter in word:
        Hlist.append(opDict[letter])
    H += weights[i] * tensor(Hlist)

#print(H)




pi = np.pi
tstart = time.time()
steps=[]


c = 0.00

#
qb0 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb1 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb3 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])

qblist = [qb0, qb1, qb2, qb3]
c_ops = colf.create_c_ops(qblist)
c_ops = []
e_ops = []
ntraj = 1
tmax= [20e-9, 200e-9]
psi0 = qbc.create_psi0(qblist, 0)
iterations = 10
initial_points = 5


def circuit(theta_arr):
    steps.append(gf.Add_step(["PY", "PY", "PY", "PY"], [0, 1, 2, 3], [theta_arr[0],theta_arr[1],theta_arr[2],theta_arr[3],]))
    steps.append(gf.Add_step(["CZnew"], [[1, 0]], [0]))
    steps.append(gf.Add_step(["PY", "CZnew"], [0, [3, 1]], [theta_arr[4], 0]))
    steps.append(gf.Add_step(["PY", "CZnew"], [0, [3, 2]], [theta_arr[5], 0]))
    steps.append(gf.Add_step(["PY", "PY"], [1, 2], [theta_arr[6], theta_arr[7]]))
    steps.append(gf.Add_step(["CZnew"], [[1, 0]], [0]))
    steps.append(gf.Add_step(["PY", "CZnew"], [0, [3, 1]], [theta_arr[8], 0]))
    steps.append(gf.Add_step(["PY", "CZnew"], [3, [1, 2]], [theta_arr[11], 0]))
    steps.append(gf.Add_step(["PY", "PY"], [1, 2], [theta_arr[9], theta_arr[10]]))

    args = {"steps": steps, "c_ops": c_ops, "e_ops": e_ops, "psi0": psi0, "Qblist": qblist, "t_max": tmax, "ntraj": ntraj, "StoreTimeDynamics": False}
    print("starts")
    state = ma.main_algorithm(args)
    #expval = np.mean(expect(H, state))
    #print(state[0])


    return -np.mean(expect(H, state))


"""def blackbox(theta_arr):
    states = circuit(theta_arr)
    print('we got states')
    print(states)
    #Ham =
    expval = np.mean(expect(H, states))

    return -np.mean(expect(H, state))
"""
def adm(t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11):
    theta_arr = [t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11]

    return circuit(theta_arr)

upperb = 4*np.pi
lowerb = -4*np.pi

pbounds = {'t0': (lowerb, upperb), 't1': (lowerb, upperb), 't2': (lowerb, upperb), 't3': (lowerb, upperb),'t4': (lowerb, upperb), 't5': (lowerb, upperb), 't6': (lowerb, upperb), 't7': (lowerb, upperb), 't8': (lowerb, upperb), 't9': (lowerb, upperb), 't10': (lowerb, upperb), 't11': (lowerb, upperb)}

new_optimizer = BayesianOptimization(
    f=adm,
    pbounds = pbounds,
    verbose=2,
    random_state=1
)


new_optimizer.maximize(
    init_points= initial_points,
    n_iter= iterations,
)
    
    
    

print("--- %s seconds ---" % (time.time() - tstart))
print( "Trajectories:" ,(ntraj), "noise:", (c), "initpoints:", (initial_points), "iterations:" ,(iterations) )
print(new_optimizer.max)
no = new_optimizer.max["params"]
x,y = {},{}
for key in no.keys():
    if len(key) == 2:
        x[key] = no[key]
    elif len(key) == 3:
        y[key] = no[key]

no = {**x,**y}
df = pd.DataFrame.from_dict(no, orient = "index").transpose()
df.to_excel("temporaryBenchmmarkOutput.xlsx")
print('done')




