# """
# Created 20231203
# Author: Serge Zaugg
# """

import xco 
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'C:/temp_xc_projects/proj04')
# Check where data will be retrieved
xc.XC_API_URL
# Check where data will be written 
xc.start_path
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json')




# Get information of what would be downloaded
df_summary, records_list = xc.get_summary(params_json = 'download_criteria.json')


df_summary.shape

len(records_list)
records_list[5]


# Download mp3 files with metadata  


xc.download(recs_pool=records_list)








# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
# Extract spectrograms of fixed-length segments and store as PNG
xc.extract_spectrograms(target_fs = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 400, equalize = False, colormap='viridis')


# get info 
help(xc.make_param)
help(xc.get)
help(xc.mp3_to_wav)
help(xc.extract_spectrograms)


