from matplotlib import pyplot as plt
import re 
import numpy as np

"""Started to create a file to directly import the data from the different simulation,
but it was difficult and took too long"""

with open("plotdata_b_longrun.txt") as f: # Reads the entire file as one string
    content_b = f.read()

with open("plotdata_c_longrun.txt") as f: # Reads the entire file as one string
    content_c = f.read()

# Splits the text document into multiple strings with the different data
str1, gamma_vec_b, beta_vec_b, exp_mat_b, minima_b, coord_b, beta_vec_b, zz_b, zo_b, oz_b, oo_b = re.split(".+=", content_b)

str1, gamma_vec_c, beta_vec_c, exp_mat_c, minima_c, coord_c, beta_vec_c, zz_c, zo_c, oz_c, oo_c = re.split(".+=", content_c)


def reWriteVector(vec):
    vec = re.sub(' +', ' ', vec) # removes eccess blank spaces
    vec = vec.replace(" ", ",") # replaces the last blank space with a comma
    vec = vec[1:] # removes the first character i.e. '['
    vec = vec[:-1] # same for the last ']'
    vec = [float(n) for n in vec[1:-1].split(",")] # creates list of floats from the string
    return vec

def reWriteMatrix(mat):
    mat = mat.replace('\n', "") # removes \n from the exp_mat matrix
    mat = re.sub(' +', ' ', mat) # removes eccess blank spaces
    mat = mat.replace(" ", ",") # replaces the last blank space with a comma
    #mat = mat.replace("[", "")
    #mat = mat.replace("]","")
    mat = mat[2:]
    mat = mat[:-1]
    #mat = re.sub("]", "]]", mat)
    #print(mat)
    rows = re.split("[\]\[]", mat)
    rows = list(filter((",").__ne__, rows))
    #print(rows)
    #matrix = np.zeros((len(rows),len(rows[1])))
    matriz = []
    for i in range(1,len(rows)-1):
        #matrix[i] = [float(n) for n in mat[1:-1].split(",")] # creates list of floats from the string
        row = rows[i]
        #print(i)
        #print(row,"hej")
        #row = row[1:] # removes the first character i.e. '['
        #row = row[:-1] # same for the last ']'
        matrix_row = [float(n) for n in row[1:-1].split(",")] # creates list of floats from the string
        matriz.append(matrix_row)
    mat = matriz
    return mat

gamma_vec_b = reWriteVector(gamma_vec_b)
beta_vec_b = reWriteVector(beta_vec_b)
exp_mat_b = reWriteMatrix(exp_mat_b)


problem = 'b'

gamma_vec = gamma_vec_b
beta_vec = beta_vec_b

# plotting matrix
# plt.matshow(exp_mat, cmap = plt.get_cmap('PiYG'))  # We need to flip the matrix of we use the matshow
# Do this by putting exp_mat[beta_resolution-1-j, i] = np.mean(expect(ham, state)) in for loops!) !
fig, ax = plt.subplots(2)
cs = ax.contourf(gamma_vec_b, beta_vec_b, exp_mat_b, 400, cmap=plt.get_cmap('PiYG'), vmin=-1, vmax=1, levels=np.linspace(-1,1,345))
# This one plots the matrix with angles
cbar = fig.colorbar(cs, ticks=np.linspace(-1,1,9))
ax.set_title(f'Cost function F($\gamma$, \u03B2) for problem {problem}')
ax.set_xlabel("$\gamma_1$")
ax.set_ylabel("\u03B2$_1$")
labels = ["0", "$\pi$/2", "$\pi$"]
plt.xticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
plt.yticks([gamma_vec[0], (gamma_vec[-1] + gamma_vec[0])/2, gamma_vec[-1]], labels)
plt.show()