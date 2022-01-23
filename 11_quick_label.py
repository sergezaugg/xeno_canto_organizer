"""
Created on Sat Jun  5 15:49:12 2021
@author: serge
"""

import os
import pickle
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt




fext_dir = '/home/serge/sz_main/ml/data/xc_dev/fex/'

# all next times 
fina = 'spectro_20220123_112528_timlab.pkl'
(X_tra, Y_tra, y_str, _, labs, fex, n_label_runs) = pickle.load( open( os.path.join(fext_dir , fina), "rb" ) ) 

# check
print('X_tra.shape', X_tra.shape)    
print('Y_tra.shape', Y_tra.shape)
print('labs.shape', labs.shape)
print('n_label_runs.shape', n_label_runs.shape)
Y_tra.sum()













relabel_thld = 4


"""
Instructions
left button:    select a time point
middle boutton: go to next segment
right boutton:  remove last point
"""

for i in np.arange(0, X_tra.shape[0],1):
    print(i)
    # only label if already labelled less or equal than relabel_thld
    if n_label_runs[i] <= relabel_thld:

        # sel_label = Y_tra[i].sum(0) >= 1
        curr_label = y_str[i]  #labs[sel_label][0]
        
        # get nummerical indes of current sound-type
        st_num_index = np.where(labs == curr_label)[0].item()
        
        # loop while figure is open 
        redo = True # to re-show same spectro if uneven nb points 
        while redo:
            print('i', i)
            plt.figure(figsize = (20, 30))
            plt.imshow(X_tra[i].squeeze().T, aspect = 'auto')
            plt.title( 'i: ' + str(i) + '    ' + curr_label)        



            # get interactive point 
            cur_vals = plt.ginput(n=-1, timeout=0)
            # chekc that nb points is even
            cur_vals = [a[0] for a in cur_vals]
            if len(cur_vals)%2 == 0:
                redo = False
            else:
                print('Error nb point must be even!')
            plt.close()
        
        # update the actual label array 
        la = np.array(cur_vals)
        la.sort() # sort in-place 
        la = la.reshape((la.shape[0]//2,2))
        la = la.round().astype(int)
        
        pos_lab_index = []
        for r in la:
            pos_lab_index.extend(np.arange(r[0],r[1]).tolist())
        pos_lab_index = np.array(pos_lab_index)

        all_int_inices = np.arange(Y_tra[i].shape[0])
        # get boolean index
        ind_set_to_one = np.isin(element = all_int_inices, test_elements = pos_lab_index)
        # and set the shit to 1 where it has to 
        Y_tra[i][ind_set_to_one,:][:,st_num_index] = 1
        n_label_runs[i] += 1
        
        # plt.plot(Y_tra[i])
        # plt.show()

        # save / overwrite  
        fileNameToSave = fext_dir + fina
        allObjects = [X_tra, Y_tra, y_str, "unused", labs, fex, n_label_runs]
        pickle.dump( allObjects, open( fileNameToSave, "wb" ) )


        if i > 6:
            break





# >>> Y_tra.sum()
# 1702  2932   4580
# >>> 

