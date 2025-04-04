# --------------
# Author : Serge Zaugg
# Description : Minimalistic example of xco usage in practice 
# --------------

import xco 

# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'C:/temp_xc_projects/proj03')
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
xc.df_recs.shape
sel = xc.df_recs['smp'].astype(int)>= 48000
xc.df_recs = xc.df_recs[sel]
xc.df_recs.shape
# Download the files 
xc.download()
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 12000)
# Extract spectrograms of fixed-length segments and store as PNG
xc.extract_spectrograms(fs_tag = 12000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, max_segm_per_file = 12, equalize = True, colormap='viridis', eps = 1e-10)

# import pandas as pd
# import os 
# # re-load and explore meta-data
# df_meta = pd.read_pickle(os.path.join(xc.start_path, 'downloaded_data_meta.pkl'))
# df_meta.head()
# df_meta.shape
# df_meta['file_name_stub'][8]
# df_meta.columns
# df_meta['file-name'][8]

