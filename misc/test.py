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
xc.make_param(filename = 'asdfbsdfbsdgfbn.json')
# get information of what would be downloaded
xc.get(params_json = 'asdfbsdfbsdgfbn.json', download = False)
# download mp3 files with metadata  
xc.get(params_json = 'asdfbsdfbsdgfbn.json', download = True)
# make aggregated summary table of all mp3 files 
xc.summary(save_csv = True)
# convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
xc.mp3_to_wav(target_fs = 21568)
xc.mp3_to_wav(target_fs = 8000)
xc.mp3_to_wav(target_fs = 1024)
# extract spectrograms 


