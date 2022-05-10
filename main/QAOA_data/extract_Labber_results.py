#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import sys
try:
    import Labber
except:
    pass
import matplotlib.pyplot as plt

# In[4]:


save=False
if 'Labber' in sys.modules:
    log = Labber.LogFile(r'QAOA landscapes.hdf5')
    data = log.getData('QAOA - Cost')
    data = np.reshape(data, (4, 61, 61))
    if save:
        np.save(r'QAOA landscapes.npy', data)
else:
    data = np.load('QAOA landscapes.npy')

# In[8]:



for i in range(4):
    plt.imshow(data[i,:,:], origin='lower')
    #print(i)
    plt.show()

"""
0 = b
1 = c
2 = d
3 = a
"""

data_a = data[3,:,:]
data_b = data[0,:,:]
data_c = data[1,:,:]
data_d = data[2,:,:]