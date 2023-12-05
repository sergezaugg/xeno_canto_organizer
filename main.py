"""
Created 20231203
Author: Serge Zaugg
"""

import xco 
import os 

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
xc.mp3_to_wav(dir_tag = "20231203T183459", params_fs = 48000)

# extract spectrograms 
xc.extract_spectrograms(dir_tag = "20231203T183459", target_sampl_freq = 48000, duratSec = 5, win_siz = 2048, win_olap = 1900, seg_step_size = 0.9, colormap = 'viridis')

# get summary table of all mp3 files 
xc.summary(save_csv = True)






