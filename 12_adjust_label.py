"""
Created on Sat Jun  5 15:49:12 2021
@author: serge
"""



# fina = 'spectro_20220123_084434.pkl'

# fext_dir = '/home/serge/sz_main/ml/data/xc_dev/fex/'



# # fina = 'dnn_fex_site__XC__freq_100_5000.pkl'
# # # fext_dir = '/home/serge/sz_main/ml/data/xc_real_run_02/fex/features_20211203_213752/'
# # # fext_dir = '/home/serge/sz_main/ml/data/xc_real_run_02/fex/features_20211204_233301/'
# # fext_dir = '/home/serge/sz_main/ml/data/xc_real_run_02/fex/features_20211206_112257/'

# data_dir = fext_dir + fina
# label_pa = fext_dir + 'labels.pkl'

# # ----------------------------
# # import os
# import pickle
# import numpy as np
# # import pandas as pd 
# import matplotlib.pyplot as plt

# # ----------------------------
# # load data
# (X_tra, Y_tra, _, _, labs, fex) = pickle.load( open( data_dir, "rb" ) ) 
# X_tra = np.expand_dims(X_tra, 3)
# # check
# print('X_tra.shape', X_tra.shape)    
# print('Y_tra.shape', Y_tra.shape)
# print('labs.shape', labs.shape)
# # to avoid overflow issues
# X_tra = X_tra.astype('float32')

# # load labels 
# lab_vals = pickle.load( open( label_pa, "rb" ) ) 
# print('len(lab_vals)', len(lab_vals))
  
# # adjust labels to fit exact times defined above 

# for i in np.arange(0, len(lab_vals),1):
# #        i = 55
#     # get region start/stop 
#     la = np.array(lab_vals[str(i)])
#     la.sort() # sort in-place 
#     la = la.reshape((la.shape[0]//2,2))
#     la = la.round().astype(int)
    
#     pos_lab_index = []
#     for r in la:
#         pos_lab_index.extend(np.arange(r[0],r[1]).tolist())
#     pos_lab_index = np.array(pos_lab_index)
#     all_int_inices = np.arange(Y_tra[i].shape[0])
#     # get boolean indec ef where to set 1 to 0
#     ind_set_to_zero = np.logical_not(np.isin(element = all_int_inices, test_elements = pos_lab_index))
#     # and set the shit to 0 where it has to 
#     Y_tra[i][ind_set_to_zero,:] = 0
    
# #        # check
# #        fig, axs = plt.subplots(2, 1)
# #        axs[0].imshow(X_tra[i].squeeze().T, aspect = 'auto')
# #        axs[1].imshow(Y_tra[i].squeeze().T, aspect = 'auto')


# # save - 
# fileNameToSave = fext_dir + fina.replace('.pkl', '') + '_timlab' + '.pkl'
# allObjects = [X_tra, Y_tra, "unused", "unused", labs, fex]
# pickle.dump( allObjects, open( fileNameToSave, "wb" ) )






