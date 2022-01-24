

import xco 
# define root path 
xc = xco.XCO(start_path = '/home/serge/sz_main/ml/data/temp01')
# check stuff 
xc.XC_API_URL
xc.start_path

# create a example json parameter file, and edit it if you want.
xc.make_param()
# get summary of what would be downloaded
xc.get(params_json = 'xc02.json', params_download = False)
# download mp3 files into a timestamped directory and store the metadata with the same timestamp
xc.get(params_json = 'xc02.json', params_download = True)
# get summary table of all mp3 files 
xc.summary(save_csv = True)
# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xc.mp3_to_wav(params_fs = 48000)
# add noise to wavs for a specific sampling rate 
xc.add_noise(params_fs = 48000, params_noize = 0.05)
# extract spectrograms 
xc.extract_spectrograms(dir_tag = '_noise_48000sps_n_0.05')
# prepare for labeling (This will overwrite labels !!!)
xc.labelling_prepare_arrays(fina = 'spectro_20220124_222518.pkl') 
# do the labelling 
xc.labelling_interactive(fina = 'spectro_20220124_222518_timlab.pkl', relabel_thld = 0)









# map to original sound-types like in CAR 
st_dict = { 
    'Amazona festiva' : 'festive_amazon_call',
    'Attila bolivianus' : 'dull_capped_attila_song',
    'Cacicus cela' : 's000040',
    'Capito aurovirens' : 's000015',
    'Crotophaga major' : 's000031',
    'Crypturellus undulatus' : 'undulated_tinamou_song',
    'Glaucidium brasilianum' : 's000014',
    'Leptotila rufaxilla' : 'grayfronted_dove_song',
    'Monasa nigrifrons' : 'black_fronted_nunbird_song',
    'Myrmelastes hyperythrus' : 's000010',
    'Nasica longirostris' : 'updownsweep_2kHz_dur1s_01',
    'Nyctibius grandis' : 's000003',
    'Nyctibius griseus' : 's000021',
    'Pitangus sulphuratus' : 's000038',
    'Psarocolius angustifrons' : 's000020',
    'Ramphastos tucanus' : 's000025',
    'Taraba major' : 's000022',
    'Trogon melanurus' : 's000016',
    'Xiphorhynchus guttatus' : 's000011',
    'Xiphorhynchus obsoletus' : 's000023',
    }

xc.extract_spectrograms(dir_tag = '_noise_48000sps_n_0.05', map_sound_type_dic = st_dict)




