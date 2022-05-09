from extract_Labber_results import data_a, data_b, data_c, data_d
import numpy as np  
import sys
import re
#from ../benchmarkplots2 import reWriteMatrix

sys.path.insert(1, '../')
from benchmarkplots2 import reWriteMatrix

min_a = np.amin(data_a)
index_a = np.where(data_a == min_a)
index_a = list(zip(index_a[0], index_a[1]))

min_b = np.amin(data_b)
index_b = np.where(data_b == min_b)
index_b = list(zip(index_b[0], index_b[1]))

min_c = np.amin(data_c)
index_c = np.where(data_c == min_c)
index_c = list(zip(index_c[0], index_c[1]))

min_d = np.amin(data_d)
index_d = np.where(data_d == min_d)
index_d = list(zip(index_d[0], index_d[1]))

print("min_a = " + str(min_a))
print("index_a = " + str(index_a))

print("min_b = " + str(min_b))
print("index_b = " + str(index_b))

print("min_c = " + str(min_c))
print("index_c = " + str(index_c))

print("min_d = " + str(min_d))
print("index_d = " + str(index_d))

with open("../benchmarkDATA&PLOTS/plotdata_a_longrun.txt") as file_a:
    id_a = []
    ind_a = []
    for ln in file_a:
        if ln.startswith("minima ="):
            id_a.append(ln[9:-1])
        if ln.startswith("coord ="):
            ind_a.append(ln[8:-1])
    #content_a = file_a.read()

sim_min_a = [float(i) for i in id_a]
sim_min_a = sim_min_a[0]
sim_index_a = ind_a
sim_index_a = sim_index_a[0]

"""
content_a = re.split(".+=", content_a)
print(np.shape(content_a))
exp_mat_a = content_a[3]
exp_mat_a = reWriteMatrix(exp_mat_a)
max_a = np.amin(-exp_mat_a)
"""

#print(sim_min_a)

with open("../benchmarkDATA&PLOTS/plotdata_b_longrun6161.txt") as file_b:
    id_b = []
    ind_b = []
    for ln in file_b:
        if ln.startswith("minima ="):
            id_b.append(ln[9:-1])
        if ln.startswith("coord ="):
            ind_b.append(ln[9:-2])
    #content_b = file_b.read()
sim_min_b = [float(i) for i in id_b]
sim_min_b = sim_min_b[0]
sim_index_b = ind_b
sim_index_b = sim_index_b[0]
"""
exp_mat_b = content_b[3]
exp_mat_b = reWriteMatrix(exp_mat_b)
max_b = np.amin(-exp_mat_b)
"""
#print(sim_min_b)

with open("../benchmarkDATA&PLOTS/plotdata_c_longrun6161.txt") as file_c:
    id_c = []
    ind_c = []
    for ln in file_c:
        if ln.startswith("minima ="):
            id_c.append(ln[9:-1])
        if ln.startswith("coord ="):
            ind_c.append(ln[8:-1])
    #content_c = file_c.read()
sim_min_c = [float(i) for i in id_c]
sim_min_c = sim_min_c[0]
sim_index_c = ind_c
sim_index_c = sim_index_c[0]
"""
exp_mat_c = content_c[3]
exp_mat_c = reWriteMatrix(exp_mat_c)
max_c = np.amin(-exp_mat_c)
"""
#print(sim_min_c)

with open("../benchmarkDATA&PLOTS/plotdata_d_longrun6161.txt") as file_d:
    id_d = []
    ind_d = []
    for ln in file_d:
        if ln.startswith("minima ="):
            id_d.append(ln[9:-1])
        if ln.startswith("coord ="):
            ind_d.append(ln[9:-2])
    #content_d = file_d.read()
sim_min_d = [float(i) for i in id_d]
sim_min_d = sim_min_d[0]
sim_index_d = ind_d
sim_index_d = sim_index_d[0]
"""
exp_mat_d = content_d[3]
exp_mat_d = reWriteMatrix(exp_mat_d)
max_d = np.amin(-exp_mat_d)
"""
#print(sim_min_d)


diff_a = abs(min_a - sim_min_a)
diff_b = abs(min_b - sim_min_b)
diff_c = abs(min_c - sim_min_c)
diff_d = abs(min_d - sim_min_d)


proc_a = diff_a/abs(min_a)
proc_b = diff_b/abs(min_b)
proc_c = diff_c/abs(min_c)
proc_d = diff_d/abs(min_d)

print(proc_a)
print(proc_b)
print(proc_c)
print(proc_d)

print(sim_index_a, index_a)
print(sim_index_b, index_b)
print(sim_index_c, index_c)
print(sim_index_d, index_d)

gamma_vec = np.linspace(0, np.pi, 61)
beta_vec = np.linspace(0, np.pi, 61)

sim_gamma_a = gamma_vec[16]
sim_beta_a = beta_vec[23]
gamma_a = gamma_vec[17]
beta_a = beta_vec[22]

sim_gamma_b = gamma_vec[14]
sim_beta_b = beta_vec[15]
gamma_b = gamma_vec[16]
beta_b = beta_vec[16]

sim_gamma_c = gamma_vec[28]
sim_beta_c = beta_vec[16]
gamma_c = gamma_vec[29]
beta_c = beta_vec[14]

sim_gamma_d = gamma_vec[15]
sim_beta_d = beta_vec[54]
gamma_d = gamma_vec[15]
beta_d = beta_vec[51]

print("simulerat", "experimentellt")
print(sim_gamma_a, gamma_a)
print(sim_beta_a, beta_a)
print(sim_gamma_b, gamma_b)
print(sim_beta_b, beta_b)
print(sim_gamma_c, gamma_c)
print(sim_beta_c, beta_c)
print(sim_gamma_d, gamma_d)
print(sim_beta_d, beta_d)

print(min_a)
print(min_b)
print(min_c)
print(min_d)

print(sim_min_a)
print(sim_min_b)
print(sim_min_c)
print(sim_min_d)

print(proc_a)
print(proc_b)
print(proc_c)
print(proc_d)


"""
print(sim_gamma_a)
print(sim_beta_a)
print(gamma_a)
print(beta_a)
"""
"""
print(max_a)
print(max_b)
print(max_c)
print(max_d)
"""
"""
print(diff_a)
print(diff_b)
print(diff_c)
print(diff_d)
"""