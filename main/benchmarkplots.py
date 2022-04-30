from matplotlib import pyplot as plt
import re 
import numpy as np

"""Started to create a file to directly import the data from the different simulation,
but it was difficult and took too long"""

with open("plotdata_b.txt") as f:
    content = f.read()

str1, gamma_vec_b, beta_vec_b, exp_mat_b, minima_b, coord_b, beta_vec_b, zz_b, zo_b, oz_b, oo_b = re.split(".+=", content)
exp_mat_b = exp_mat_b.replace('\n', "")

gamma_vec_b = [float(n) for n in gamma_vec_b[1:-1].split(" ")]

print(type(gamma_vec_b))

# plotting matrix
# plt.matshow(exp_mat, cmap = plt.get_cmap('PiYG'))  # We need to flip the matrix of we use the matshow
# Do this by putting exp_mat[beta_resolution-1-j, i] = np.mean(expect(ham, state)) in for loops!) !
fig, ax = plt.subplots()
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