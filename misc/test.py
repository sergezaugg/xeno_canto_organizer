# """
# Created 20231203
# Author: Serge Zaugg
# """

import xco 

# define the root path 
xc = xco.XCO(start_path = 'C:/temp_xc_projects/proj02')
# check where data will be retrieved
xc.XC_API_URL
# check where data will be written 
xc.start_path
# create a template json parameter file (to be edited)
xc.make_param(filename = 'baba_test.json')
# get information of what would be downloaded
xc.get(params_json = 'baba_test.json', download = False)
# download mp3 files with metadata  
xc.get(params_json = 'baba_test.json', download = True)
# convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
xc.mp3_to_wav(target_fs = 21568)
xc.mp3_to_wav(target_fs = 8000)
xc.mp3_to_wav(target_fs = 1024)
# extract spectrograms 
xc.extract_spectrograms(target_fs = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 256, equalize = True)
xc.extract_spectrograms(target_fs = 21568, segm_duration = 2.0, segm_step = 1.1, win_siz = 1024, win_olap = 1000, equalize = False, colormap = "viridis")
xc.extract_spectrograms(target_fs = 8000, segm_duration = 1.5, segm_step = 0.5, win_siz = 600, win_olap = 256, equalize = True, colormap = "gray")
xc.extract_spectrograms(target_fs = 1024, segm_duration = 10.0, segm_step = 1.0, win_siz = 256, win_olap = 200, equalize = False, colormap = "inferno")






# Import xco module
import xco 
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'C:/temp_xc_projects/proj02')
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json')
# Get information of what would be downloaded
xc.get(params_json = 'download_criteria.json', download = False)
# Download mp3 files with metadata  
xc.get(params_json = 'download_criteria.json', download = True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
# Extract spectrograms of fixed-length segments and store as PNGs
xc.extract_spectrograms(target_fs = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 400, equalize = True)




