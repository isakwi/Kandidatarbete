from extract_Labber_results import data_a, data_b, data_c, data_d
import numpy as np  

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

with open("../plotdata_a_longrun.txt") as file_a:
    id_a = []
    for ln in file_a:
        if ln.startswith("minima ="):
            id_a.append(ln[9:-1])
sim_min_a = [float(i) for i in id_a]
sim_min_a = sim_min_a[0]
#print(sim_min_a)

with open("../plotdata_b_longrun6161.txt") as file_b:
    id_b = []
    for ln in file_b:
        if ln.startswith("minima ="):
            id_b.append(ln[9:-1])
sim_min_b = [float(i) for i in id_b]
sim_min_b = sim_min_b[0]
#print(sim_min_b)

with open("../plotdata_c_longrun6161.txt") as file_c:
    id_c = []
    for ln in file_c:
        if ln.startswith("minima ="):
            id_c.append(ln[9:-1])
sim_min_c = [float(i) for i in id_c]
sim_min_c = sim_min_c[0]
#print(sim_min_c)

with open("../plotdata_d_longrun6161.txt") as file_d:
    id_d = []
    for ln in file_d:
        if ln.startswith("minima ="):
            id_d.append(ln[9:-1])
sim_min_d = [float(i) for i in id_d]
sim_min_d = sim_min_d[0]
#print(sim_min_d)

diff_a = abs(min_a - sim_min_a)
diff_b = abs(min_b - sim_min_b)
diff_c = abs(min_c - sim_min_c)
diff_d = abs(min_d - sim_min_d)

print(diff_a)
print(diff_b)
print(diff_c)
print(diff_d)