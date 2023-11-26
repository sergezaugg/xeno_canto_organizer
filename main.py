

import xco 
import os 
import matplotlib.pyplot as plt  
import numpy as np
from PIL import Image

# define root path 
xc = xco.XCO(start_path = os.path.join('C:\\Users\\sezau\\Desktop\\data'))
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
xc.extract_spectrograms(dir_tag = '_wav_32000sps')  # 20231125T134336_noise_48000sps_n_0.05












X = xc.X

arr = X[0].T
arr.shape
arr = np.flip(arr, axis=0)


# normalize 
arr = arr - arr.min()
arr = np.log(arr+1.0)
arr = arr/arr.max()

# Get the color map by name:
# plt.col ormaps()
# map_val = 'viridis'
# map_val = 'magma'
map_val = 'inferno'
# map_val = 'plasma'
# map_val = 'twilight'

cm = plt.get_cmap(map_val)

# Apply the colormap like a function to any array:
colored_image = cm(arr)
im = Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8))
# save as image 
im.save(os.path.join(xc.start_path, "test_image_dev_01.png"))






