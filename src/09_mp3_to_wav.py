#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:51:46 2020
@author: serge
"""

import os 
import subprocess
import numpy as np 
import librosa
import soundfile as sf

source_path = '/home/serge/sz_main/ml/data/xc_spec_03/'
destin_path = source_path + 'wav/'
destin_path_noiz = destin_path + 'noized/'

all_mp3s = os.listdir(source_path)
all_mp3s = [a for a in all_mp3s if '.mp3' in a]

for finam in all_mp3s:
    outnam = finam.replace('.mp3','.wav' )
    # mp3 to wav stereo to mono convert 48000
    try:
        subprocess.call(['ffmpeg', '-i', source_path + finam, 
                         '-ar', '48000', '-ac', '1', 
                         destin_path + outnam])
    except:
        print("an exception occured")

#ffmpeg -i 'Glaucidium brasilianum.mp3' _new.wav
#ffmpeg -i 'Glaucidium brasilianum.mp3' -ar 48000 _new2.wav
#ffmpeg -i 'Glaucidium brasilianum.mp3' -ar 48000 -ac 1 _new3.wav

# sudo apt  install ffmpeg  # version 7:4.2.4-1ubuntu0.1



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


        
        
        
        
        
        
        

