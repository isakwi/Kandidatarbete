import numpy as np
import GateFuncs as gf 

gamma = [1,1]
J = 1

steps = []

steps.append(gf.Add_step(["HD"], [1], [2*gamma_i * J]))
#steps.append(gf.Add_step(["CZ"]))

"""
This is meant to be a file to easily implement the benchmark. I don't know if this is how 
we want to do it, but then we can just remove the file // Albin
"""