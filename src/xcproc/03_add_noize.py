#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 20211010
@author: serge Zaugg
"""









#-----------------
# make some noize 
        
def add_noise(fi, painp , paout, noize_fac = 0.1):
    data, fs = librosa.load(os.path.join(painp,fi), sr=None)
    print(fs)
    
    # truncate to max duration
    max_dur_sec = 20
    max_dur_smp = (max_dur_sec * fs) + 1000
    data = data[0:max_dur_smp]
    
    # add noize 
    noiz_std = noize_fac*data.std()
    noiz = np.random.normal(loc=0.0, scale=noiz_std, size=data.shape[0])
    data = data + noiz
    # Write   
    fin = fi.replace('.wav', '') + '.wav' 
    sf.write(os.path.join(paout, fin), data, fs)

all_wavs = os.listdir(destin_path)
all_wavs = [a for a in all_wavs if '.wav' in a]
for finam in all_wavs:
    print(destin_path + finam)
    add_noise(finam, destin_path, destin_path_noiz, noize_fac = 0.05)
