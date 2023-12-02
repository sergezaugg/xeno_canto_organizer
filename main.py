
import xco 
import os 
import matplotlib.pyplot as plt  
import numpy as np
from PIL import Image

# define root path 
xc = xco.XCO(start_path = os.path.join('C:\\Users\\sezau\\Desktop\\data2'))
# check stuff 
xc.XC_API_URL
xc.start_path
 
# create a example json parameter file, and edit it if you want.
xc.make_param()

# get summary of what would be downloaded
xc.get(params_json = 'example.json', params_download = False)

# download mp3 files into a timestamped directory and store the metadata with the same timestamp
xc.get(params_json = 'example.json', params_download = True)

# get summary table of all mp3 files 
xc.summary(save_csv = True)

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xc.mp3_to_wav(params_fs = 32000)

# extract spectrograms 
xc.extract_spectrograms(dir_tag = '_wav_32000sps')  


