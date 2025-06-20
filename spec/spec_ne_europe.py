#----------------------
# Author : Serge Zaugg
# Description : Example of xco usage in practice 
#----------------------

# Make an instance of the XCO class and define the start path 
import xco 
xc = xco.XCO(start_path = 'd:/xc_real_projects/xc_ne_europe')
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_ne_europe.json', template = "n_europe")
# Get information of what will be downloaded
xc.download_summary(params_json = 'download_ne_europe.json')
# make summary tables 
print(xc.df_recs.shape)
# keep only if fs large enough 
sel = xc.df_recs['smp'].astype(int)>= 24000
xc.df_recs = xc.df_recs[sel]
# Download the files 
xc.download_audio_files()
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Make long spectrogram 128 freq x 1152 time (1024+128= 1152)
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, max_segm_per_file = 20, equalize = True, colormap='viridis')


