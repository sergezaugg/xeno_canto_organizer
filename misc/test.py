# """
# Created 20231203
# Author: Serge Zaugg
# """

import xco 

# define the root path 
xc = xco.XCO(start_path = 'C:/xc_real_projects/xc_aec_project')
# check where data will be retrieved
xc.XC_API_URL
# check where data will be written 
xc.start_path
# create a template json parameter file (to be edited)
xc.make_param(filename = 'xc_aec_proj.json')
# get information of what would be downloaded
xc.get(params_json = 'xc_aec_proj.json', download = False)
# download mp3 files with metadata  
xc.get(params_json = 'xc_aec_proj.json', download = True)
# convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
# extract spectrograms 
xc.extract_spectrograms(target_fs = 24000, segm_duration = 0.5, segm_step = 1.0, win_siz = 256, win_olap = 192, equalize = True, colormap='viridis')








