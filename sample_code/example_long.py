# --------------
# Author : Serge Zaugg
# Description : Demo examples of xco usage in practice
# For real projects please use a dir outside if this repo
# --------------

#---------------------------------------
import os
import pandas as pd
import xeno_canto_organizer.xco as xco

# make a projects dir, if it does not already exist
if not os.path.isdir('./temp_xc_project'):
    os.makedirs('./temp_xc_project')
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = './temp_xc_project')
# Check where data will be written 
xc.start_path
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json', template = "mini")
# Get summary table of what will be downloaded into xc.df_recs
xc.download_summary(params_json = 'download_criteria.json')
# (if session was closed) reload summary from local pkl file into xc.df_recs
xc.reload_local_summary()
# (optional) Make summaries of what will be downloaded
print(xc.df_recs.shape)
print(xc.df_recs.head(10))
print(xc.df_recs['gen'].value_counts())
# (optional) list can be filtered prior to download based on metadata, e.g. keep only if fs large enough 
sel = xc.df_recs['smp'].astype(int)>= 24000
xc.df_recs = xc.df_recs[sel]
# Download the files 
xc.download_audio_files()
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, max_segm_per_file = 12, 
                        equalize = True, colormap='viridis', eps = 1e-10)
# (optional) load and explore meta-data
df_meta = pd.read_pickle(os.path.join(xc.start_path, 'downloaded_data_meta.pkl'))
df_meta.head()
# End of the process
# You can close session

#---------------------------------------
# Open a new session
# The pre-downloaded mp3 files can be reprocessed with different parameters 
# Point XCO to the dir with pre-downloaded mp33
xc = xco.XCO(start_path = './temp_xc_project')

# Make wavs with fs = 20000 and then short spectrogram 
xc.mp3_to_wav(conversion_fs = 20000)
xc.extract_spectrograms(fs_tag = 20000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, win_olap = 220.5, max_segm_per_file = 20, 
                        equalize = True, colormap='gray')

# Make  Make wavs with fs = 16000 and then long spectrogram 
xc.mp3_to_wav(conversion_fs = 16000)
xc.extract_spectrograms(fs_tag = 16000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, max_segm_per_file = 20, 
                        equalize = False, colormap='viridis')






