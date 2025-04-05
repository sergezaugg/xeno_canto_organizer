# --------------
# Author : Serge Zaugg
# Description : Example of xco usage in practice just as a demo
# For a real project use a dir outside if this repo
# --------------

import os
import pandas as pd
import xco 

# make a projects dir, if it does not already exist
if not os.path.isdir('./temp_xc_project'):
    os.makedirs('./temp_xc_project')
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = './temp_xc_project')
# Check where data will be retrieved
xc.XC_API_URL
# Check where data will be written 
xc.start_path
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json', template = "mini")
# Get information of what will be downloaded
xc.get_summary(params_json = 'download_criteria.json')
# Make summaries  
print(xc.df_recs.shape)
print(xc.df_recs.head(10))
# keep only if fs large enough 
sel = xc.df_recs['smp'].astype(int)>= 24000
xc.df_recs = xc.df_recs[sel]
# Download the files 
xc.download()
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, max_segm_per_file = 12, equalize = True, colormap='viridis', eps = 1e-10)
# Re-load and explore meta-data
df_meta = pd.read_pickle(os.path.join(xc.start_path, 'downloaded_data_meta.pkl'))
df_meta.head()




# Make spectrogram with size = 128 x 128 
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, win_olap = 220.5, max_segm_per_file = 20, equalize = True, colormap='gray')

# Make long spectrogram 128 freq x 1152 time (1024+128= 1152)
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, max_segm_per_file = 20, equalize = True, colormap='gray')

# Make rectangular spectrogram with size = 128 freq x 256 time 
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 0.394 , segm_step = 0.25, win_siz = 256, win_olap = 220.5, max_segm_per_file = 20, equalize = True, colormap='gray')






