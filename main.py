
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

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xc.mp3_to_wav(dir_tag = "20231203T182524", params_fs = 32000)

# extract spectrograms 
xc.extract_spectrograms(dir_tag = "20231203T182524", target_sampl_freq = 32000, duratSec = 5, win_siz = 1024, win_olap = 512+256, colormap = 'viridis')
xc.extract_spectrograms(dir_tag = "20231203T182524", target_sampl_freq = 32000, duratSec = 5, win_siz = 2048, win_olap = 1900, colormap = 'viridis')

# get summary table of all mp3 files 
xc.summary(save_csv = True)






