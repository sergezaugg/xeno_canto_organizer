


import src.xco as x

xco = x.XCO()

xco.XC_API_URL
xco.start_path


# create a example json parameter file, and edit it if you want.
xco.xco_make_param()

# get summary of what would be downloaded
xco.xco_get(params_json = 'e2.json', params_download = False)

# download mp3 files into a timestamped directory and store the metadata with the same timestamp
xco.xco_get(params_json = 'e2.json', params_download = True)

# get summary table of all mp3 files 
xco.xco_summary()

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xco.xco_m2w(params_fs = 48000)

# add noise to wavs for a specific sampling rate 
xco.xco_add_noise(params_fs = 48000, params_noize = 0.1)




