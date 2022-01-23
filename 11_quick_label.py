"""
Created on Sat Jun  5 15:49:12 2021
@author: serge
"""

# ----------------------------
import os
import pickle
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

fina = 'spectro_20220123_084434.pkl'

fext_dir = '/home/serge/sz_main/ml/data/xc_dev/fex/'






data_dir = fext_dir + fina
label_pa = fext_dir + 'labels.pkl'

# ----------------------------
# load data
(X_tra, Y_tra, _, _, labs, fex) = pickle.load( open( data_dir, "rb" ) ) 
X_tra = np.expand_dims(X_tra, 3)
# check
print('X_tra.shape', X_tra.shape)    
print('Y_tra.shape', Y_tra.shape)
print('labs.shape', labs.shape)
# to avoid overflow issues
X_tra = X_tra.astype('float32')


#-------------------------------------
# quick loop over spectrograms and get labels 

# load partial labels, if available 
if os.path.isfile(label_pa):
    lab_vals = pickle.load( open( label_pa, "rb" ) ) 
    # get index from which to continue 
    last_index = np.array([a for a in lab_vals.keys()]).astype('int').max()
    star_index = last_index + 1
else:
    lab_vals = {}
    star_index = 0

"""
Instructions
left button:    select a time point
middle boutton: go to next segment
right boutton:  remove last point
"""
for i in np.arange(star_index, X_tra.shape[0],1):
    print
    redo = True # to re-show same spectro if uneven nb points 
    while redo:
        print('i', i)
        plt.figure(figsize = (20, 30))
        plt.imshow(X_tra[i].squeeze().T, aspect = 'auto')
        # 
        sel_label = Y_tra[i].sum(0) >= 1
        curr_label = labs[sel_label][0]
        plt.title(curr_label)
        # get interactive point 
        cur_vals = plt.ginput(n=-1, timeout=0)
        # remove freq info 
        cur_vals = [a[0] for a in cur_vals]
        if len(cur_vals)%2 == 0:
            redo = False
        else:
            print('Error nb point must be even!')
        plt.close()
    
    lab_vals[str(i)] = cur_vals
    pickle.dump( lab_vals, open( label_pa, "wb" ) )
    
    


  






