# --------------
# Author : Serge Zaugg
# Description : Minimalistic example. Downloads 10 files and makes 111 small spectrograms
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
df_records = xc.get_summary(params_json = 'download_criteria.json')

# make summaries  
print(df_records.shape)
print(df_records['full_spec_name'].value_counts())
print(df_records['cnt'].value_counts())
print(df_records['lic'].value_counts())

# Download the files 
xc.download(df_recs = df_records)

# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 20000)
# Extract spectrograms of fixed-length segments and store as PNG
xc.extract_spectrograms(target_fs = 20000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, equalize = True, colormap='viridis', eps = 1e-10)

import pandas as pd
import os
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# re-load and explore meta-data
df_meta = pd.read_pickle(os.path.join(xc.start_path, 'downloaded_data_meta.pkl'))
df_meta.head()
df_meta.shape
df_meta['file_name_stub'][1]










