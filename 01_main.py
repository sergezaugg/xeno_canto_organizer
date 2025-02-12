"""
Created 20231203
Author: Serge Zaugg
"""

import xco 
import os 

# define root path 
xc = xco.XCO(start_path = os.path.join('C:\\Users\\sezau\\Desktop\\proj04'))
# check stuff 
xc.XC_API_URL
xc.start_path
# create a template json parameter file, and edit it if you want.
xc.make_param()
# get information of will would be downloaded
xc.get(params_json = 'download_params.json', download = False)
# download mp3 files into a time-stamped directory and store the metadata with the same timestamp
xc.get(params_json = 'download_params.json', download = True)
# get aggregated summary table of all mp3 files 
xc.summary(save_csv = True)
# convert mp3s to wav with a specific sampling rate 
xc.mp3_to_wav(target_fs = 24000)
# extract spectrograms 
xc.extract_spectrograms(target_sampl_freq = 24000, duratSec = 0.5, win_siz = 256, win_olap = 128, seg_step_size = 0.5, colormap = 'viridis')











