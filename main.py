
import xco as x

# define root path 
xco = x.XCO(start_path = '/home/serge/sz_main/ml/data/xc_dev')

# check stuff 
xco.XC_API_URL
xco.start_path

# create a example json parameter file, and edit it if you want.
xco.make_param()

# get summary of what would be downloaded
xco.get(params_json = '3.json', params_download = False)

# download mp3 files into a timestamped directory and store the metadata with the same timestamp
xco.get(params_json = '2.json', params_download = True)

# get summary table of all mp3 files 
xco.summary()

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xco.mp3_to_wav(params_fs = 48000)

# add noise to wavs for a specific sampling rate 
xco.add_noise(params_fs = 48000, params_noize = 0.05)

# extract spectrograms 
xco.extract_spectrograms(summary_file = 'summary_20220123T084349.csv', dir_tag = '_noise_48000sps_n_0.05')




