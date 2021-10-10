#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created 20211010
@author: serge Zaugg
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





        
        
        
        
        
        
        

