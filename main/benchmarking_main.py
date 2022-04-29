import time
import matplotlib.pyplot as plt
import readData as rd
import qubitClass as Qb
import numpy as np
import collapseOperatorFunction as co
from qutip import *
import gateFuncs as gf
import mainAlgorithm as mA
pi = np.pi


def benchmarking(Qblist):
    c_ops = co.createCollapseOperators(Qblist)
    psi0 = 1  # Some initial state
    n = 5000  # Number of iterations
    F = 1  # Some cost function
    J = 1
    gamma = 1
    beta = 1
    for iteration in range(n):
        p=0 # tvungen att lägga in för att kunna köra (indentation)
        # Do some quantum algorithm
        # Do measurements
        # Optimize cost function
        # Prepare new psi0
