# """
# Author: Serge Zaugg
# Description : manual tests
# """

import xco 

# define the root path 
xc = xco.XCO(start_path = "C:/temp_xc_projects/proj05")
# check where data will be retrieved
xc.XC_API_URL
# check where data will be written 
xc.start_path
# create a template json parameter file (to be edited)
xc.make_param(filename = 'aaaaaaaaaaa.json')
# get information of what would be downloaded
xc.get(params_json = 'test_test.json', download = False)
# download mp3 files with metadata  
xc.get(params_json = 'test_test.json', download = True)
# convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)

xc.mp3_to_wav(target_fs = 24000)
xc.extract_spectrograms(target_fs = 24000, segm_duration = 0.5, segm_step = 0.5, win_siz = 256, win_olap = 164, equalize = True, colormap='gray')

xc.mp3_to_wav(target_fs = 16000)
xc.extract_spectrograms(target_fs = 16000, segm_duration = 3.0, segm_step = 3.0, win_siz = 512, win_olap = 256, equalize = True, colormap='viridis')




# Import xco module
import xco 
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = "C:/temp_xc_projects/proj05")
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json')
# Get information of what would be downloaded
xc.get(params_json = 'download_criteria.json', download = False)
# Download mp3 files with metadata  
xc.get(params_json = 'download_criteria.json', download = True)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
# Extract spectrograms of fixed-length segments and store as PNGs
xc.extract_spectrograms(target_fs = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 256, equalize = True)






