from scipy.io import loadmat
import numpy as np

mat_dict={}
mat_dict.update(loadmat('structure.mat'))
goodtrx=mat_dict['structure'][0]

currentfly=1
currframe= 10
first_frame= goodtrx[0][0,0]
idx_to_draw= currframe-first_frame
goodtrx[currentfly-1][0,1]
print goodtrx[currentfly-1][0,1]
print idx_to_draw



