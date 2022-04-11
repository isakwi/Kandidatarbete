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
pi = np.pi
tstart = time.time()
steps=[]


c = 0.01

#
qb0 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb1 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])
qb2 = qbc.Qubit(3, [c, c, c], -229e6 * 2 * pi, [1,1], [1,0,0])
qb3 = qbc.Qubit(3, [c, c, c], -225e6 * 2 * pi, [2,2], [1,0,0])

def circuit(theta_arr):
    steps.append(gf.Add_step(["PY", "PY", "PY", "PY"], [0, 1, 2, 3], [theta_arr[0],theta_arr[1],theta_arr[2],theta_arr[3],]))
    steps.append(gf.Add_step(["CZnew"], [[1,0]], [0]))
    steps.append(gf.Add_step(["PY", "CZnew"], [[0], [3,1]] ,[theta_arr[4], 0]))
