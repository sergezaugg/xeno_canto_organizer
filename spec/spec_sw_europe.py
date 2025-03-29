#----------------------
# 
#----------------------

# Make an instance of the XCO class and define the start path 
import xco 

xc = xco.XCO(start_path = 'C:/xc_real_projects/xc_sw_europe')

# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_sw_europe_small.json', template = "sw_europe_small")

# Get information of what will be downloaded
df_records = xc.get_summary(params_json = 'download_sw_europe_small.json')

# make summary tables 
print(df_records.shape)
print(df_records['full_spec_name'].value_counts())
print(df_records['cnt'].value_counts())
print(df_records['lic'].value_counts())

# Download the files 
xc.download(df_recs=df_records)

# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(target_fs = 24000)

# Make spectrogram with size = 128 x 128 
xc.extract_spectrograms(target_fs = 24000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, win_olap = 220.5, equalize = True, colormap='gray')

# Make long spectrogram 128 freq x 1152 time (1024+128= 1152)
xc.extract_spectrograms(target_fs = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, equalize = True, colormap='gray')

# Make rectangular spectrogram with size = 128 freq x 256 time 
xc.extract_spectrograms(target_fs = 24000, segm_duration = 0.394 , segm_step = 0.25, win_siz = 256, win_olap = 220.5, equalize = True, colormap='gray')




import pandas as pd
import os 

# re-load and explore meta-data
df_meta = pd.read_pickle(os.path.join(xc.start_path, 'downloaded_data_meta.pkl'))
df_meta.head()
df_meta.shape
df_meta['file_name_stub'][100]
df_meta.columns

