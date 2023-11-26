

import xco 
import os 

# define root path 
xc = xco.XCO(start_path = os.path.join('C:\\Users\\sezau\\Desktop\\data'))
# check stuff 
xc.XC_API_URL
xc.start_path


   
# create a example json parameter file, and edit it if you want.
xc.make_param()

# get summary of what would be downloaded
xc.get(params_json = 'xc02.json', params_download = False)

# download mp3 files into a timestamped directory and store the metadata with the same timestamp
xc.get(params_json = 'xc02.json', params_download = True)

# get summary table of all mp3 files 
xc.summary(save_csv = True)

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xc.mp3_to_wav(params_fs = 48000)

# add noise to wavs for a specific sampling rate 
xc.add_noise(params_fs = 48000, params_noize = 0.05)

# extract spectrograms 
xc.extract_spectrograms(dir_tag = '_noise_48000sps_n_0.05')  # 20231125T134336_noise_48000sps_n_0.05





