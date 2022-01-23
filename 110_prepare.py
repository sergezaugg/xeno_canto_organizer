


import os
import pickle
import numpy as np

fext_dir = '/home/serge/sz_main/ml/data/xc_dev/fex/'
fina = 'spectro_20220123_112528.pkl'

# load data first time 
(X_tra, Y_tra, y_str, _, labs, fex) = pickle.load( open( os.path.join(fext_dir , fina), "rb" ) ) 
X_tra = X_tra.astype('float32')
X_tra = np.expand_dims(X_tra, 3)
n_label_runs = np.zeros(X_tra.shape[0], dtype='int')
Y_tra[:] = 0

# save / overwrite  
fileNameToSave = fext_dir + fina.replace('.pkl', '') + '_timlab' + '.pkl'
allObjects = [X_tra, Y_tra, y_str, "unused", labs, fex, n_label_runs]
pickle.dump( allObjects, open( fileNameToSave, "wb" ) )




