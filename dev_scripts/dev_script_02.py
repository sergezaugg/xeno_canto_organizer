# --------------
# Author : Serge Zaugg
# Description : For devel only : assess code in interactive mode 
# --------------

import os
import src.xeno_canto_organizer.xco as xco
# make a projects dir, if it does not already exist
if not os.path.isdir('d:/xc_real_projects/test'):
    os.makedirs('d:/xc_real_projects/test')
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'd:/xc_real_projects/test')
# Create a template json parameter file (to be edited) and a dict in current session
# dl_par = xc.make_param(filename = 'download_criteria.json', template = "mini")
# Get summary table of what will be downloaded into xc.df_recs
# xc.download_summary(download_params = 'download_criteria.json', verbose = False)
# same usinf a dict in-session
# xc.download_summary(download_params = dl_par, verbose = False)
# optional
# xc.reload_local_summary()
# Download the files 
# xc.download_audio_files(verbose = False)
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000, verbose = False)

len(xc.failed_wav_conv_li)

# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, 
                        win_olap = 192, max_segm_per_file = 12, 
                        equalize = True, colormap='viridis', verbose = False, eps = 1e-10)

xc.extract_spectrograms(fs_tag = 24000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, 
                        win_olap = 220.5, max_segm_per_file = 20, 
                        equalize = True, colormap='gray',  verbose = False)

xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, 
                        win_olap = 220.00, max_segm_per_file = 20, 
                        equalize = False, colormap='viridis')






