# --------------
# Author : Serge Zaugg
# Description : 
# --------------

import pandas as pd
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

#----------------------
# Minimalistic example. Downloads 10 files and makes 111 small spectrograms
import xco 
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'C:/temp_xc_projects/proj03')
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json', template = "mini")
# Get information of what will be downloaded
df_records = xc.get_summary(params_json = 'download_criteria.json')
# make summaries  
print(df_records.shape)
# Download the files 
xc.download(df_recs = df_records)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 20000)
# Extract spectrograms of fixed-length segments and store as PNG
xc.extract_spectrograms(target_fs = 20000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, equalize = True, colormap='viridis', eps = 1e-10)


#----------------------
# A FULL example! Downloads 897 files from passerines of northern Europe and makes 48082 small spectrograms
# Possible use case : to do real work with deep neural networks for unsupervised clustering 
import xco 
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'C:/temp_xc_projects/proj04')
# Check where data will be retrieved
xc.XC_API_URL
# Check where data will be written 
xc.start_path
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_n_europe.json', template = "n_europe")
# Get information of what will be downloaded
df_records = xc.get_summary(params_json = 'download_n_europe.json')
# make summary tables 
print(df_records.shape)
print(df_records['full_spec_name'].value_counts())
print(df_records['cnt'].value_counts())
print(df_records['lic'].value_counts())
# Download the files 
xc.download(df_recs=df_records)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)
# Make spectrogram with size = 128 x 128 and 1 channel
xc.extract_spectrograms(target_fs = 24000, segm_duration = 0.5, segm_step = 0.5, win_siz = 256, win_olap = 164, equalize = True, colormap='gray')










