import time
import matplotlib.pyplot as plt
import read_data as rd
import Qb_class as Qb
import numpy as np
import CollapseOperator_function as co
from qutip import *
import GateFuncs as gf
import main_Algorithm as mA
pi = np.pi


def benchmarking(Qblist):
    c_ops = co.create_c_ops(Qblist)
    psi0 = 1  # Some initial state
    n = 5000  # Number of iterations
    F = 1  # Some cost function
    J = 1
    gamma = 1
    beta = 1
    for iteration in range(n):
        # Do some quantum algorithm
        # Do measurements
        # Optimize cost function
        # Prepare new psi0
