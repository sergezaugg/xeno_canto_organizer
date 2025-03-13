

#----------------------
# A FULL example! Downloads 897 files from passerines of northern Europe and makes 48082 small spectrograms
# Possible use case : to do real work with deep neural networks for unsupervised clustering 
import xco 
# Make an instance of the XCO class and define the start path 

# xc = xco.XCO(start_path = 'C:/xc_real_projects/xc_aec_project_n_europe')
# xc = xco.XCO(start_path = 'C:/xc_real_projects/xc_aec_project_sw_europe')
xc = xco.XCO(start_path = 'C:/xc_real_projects/xc_aec_n_eur_longclips')

# Check where data will be retrieved
xc.XC_API_URL
# Check where data will be written 
xc.start_path
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_n_europe.json', template = "n_europe")
# xc.make_param(filename = 'download_sw_europe.json', template = "sw_europe")
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

# # Make spectrogram with size = 128 x 128 and 1 channel
# xc.extract_spectrograms(target_fs = 24000, segm_duration = 0.202, segm_step = 0.5, win_siz = 256, win_olap = 220.5, equalize = True, colormap='gray')

# Make long spectrogram 128 freq x 1152 time (1024+128= 1152)
xc.extract_spectrograms(target_fs = 24000, segm_duration = 1.738, segm_step = 0.95, win_siz = 256, win_olap = 220.00, equalize = True, colormap='gray')



