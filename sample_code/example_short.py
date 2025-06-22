# --------------
# Author : Serge Zaugg
# Description : Minimalistic demo example of xco usage in practice
# For real projects we recommend using a dir outside if this repo
# --------------

# install xco package from github
# pip install https://github.com/sergezaugg/xeno_canto_organizer/releases/download/v0.9.15/xeno_canto_organizer-0.9.15-py3-none-any.whl

import os
import xeno_canto_organizer.xco as xco

# make a projects dir, if it does not already exist
if not os.path.isdir('./temp_xc_project'):
    os.makedirs('./temp_xc_project')
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = './temp_xc_project')
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json', template = "mini")
# Get summary table of what will be downloaded into xc.df_recs
xc.download_summary(download_params = 'download_criteria.json')
# Download the files 
xc.download_audio_files()
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(
    fs_tag = 24000, 
    segm_duration = 1.0, 
    segm_step = 0.5, 
    win_siz = 512, 
    win_olap = 192, 
    max_segm_per_file = 12, 
    equalize = True, 
    colormap='viridis', 
    )








