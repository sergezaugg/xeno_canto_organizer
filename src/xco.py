"""
Created 20211010
@author: serge Zaugg
"""

import os
# import sys
import re
import json
import requests
import pandas as pd
import unidecode
import datetime 
import argparse

import subprocess
import numpy as np 
# import librosa
import soundfile as sf





# constant parameters
XC_API_URL = 'https://www.xeno-canto.org/api/2/recordings'

# helper functions 
def convsec(x):
    """Convert 'mm:ss' (str) to seconds (int)"""
    x = x.split(':')
    x = int(x[0])*60 + int(x[1])
    return(x)




# evalutes to False in interactive mode and True in script mode 
import __main__ as main_module
cli_call = hasattr(main_module, '__file__')
if cli_call:
    start_path = os.getcwd() # get dir from which script was called 
else: # devel 
    start_path = '/home/serge/sz_main/ml/data/xc_spec_03' 


# main function to download mp3 from XC, or just get a summary
def xco_get():

    main_download_path = os.path.join(start_path, 'downloads')

    if not os.path.exists(main_download_path):
        os.mkdir(main_download_path)


    # parse CLI arguments
    if cli_call:
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('params_json', type=str, help='required, parameter file name (.json), can include relative path')
        parser.add_argument('-d', '--download', action='store_true', help='set -d to download files, else only a summary will be returned')
        args = parser.parse_args()
        params_json = args.params_json
        params_download = args.download
    else: # devel 
        params_json = "example.json"
        params_download = False
        print(params_json)
        print(params_download)

 

    # load parameters from json file 
    with open(os.path.join(start_path, params_json)) as f:
        dl_params = json.load(f)

   



    if params_download:
        # Create time-stamped directory where files will be downloaded
        timstamp = 'download_' + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')   
        source_path = os.path.join(main_download_path, timstamp)
        if not os.path.exists(source_path):
            os.mkdir(source_path)
        print("Retrieving info from xc and downloading ...")    
        # make a copy of parameter file
        with open(os.path.join(main_download_path, timstamp + '_params.json'), 'w') as fp:
            json.dump(dl_params, fp,  indent=4)
    else:
        print("Retrieving info from xc ...")




    df_all = pd.DataFrame()
    for cnt in dl_params['country']:
        cnt_str = '+cnt:' + cnt

        for ke in dl_params['species']:        
            search_str = ke.replace(' ', '+') 
            tag = search_str.replace('+','_') + '_'
            
            full_query_string = XC_API_URL + '?query=' + search_str + cnt_str
            r = requests.get(full_query_string, allow_redirects=True)

            j = r.json()
            recs = j['recordings']

            # exclude if length no in specified range 
            recs = [a for a in recs if convsec(a["length"]) > dl_params['min_duration_s'] and convsec(a["length"]) <= dl_params['max_duration_s']]
            
            # excude files with no-derivative licenses
            if dl_params['exclude_nd']:
                recs = [a for a in recs if not 'nd' in a['lic'].lower()]

            # select based on quality rating of recordings
            recs = [a for a in recs if a['q'] in dl_params['quality']]





            # download 
            if params_download:
                for re_i in recs:
                    # print(len(re_i["also"]))
                    re_i["also"] = ' + '.join(re_i["also"])
                    # print(re_i["file"])
                    length_s = convsec(re_i["length"])

                    full_download_string = 'http:' + re_i["file"]

                    r = requests.get(full_download_string, allow_redirects=True)

                    # simplify filename stem 
                    finam2 = re_i["file-name"].replace('.mp3', '')
                    finam2 = unidecode.unidecode(finam2)
                    finam2 = finam2.replace(' ', '_').replace('-', '_')
                    finam2 = re.sub(r'[^a-zA-Z0-9_]', '', finam2)
                    finam2 = tag + finam2

                    open(os.path.join(source_path, finam2 + '.mp3') , 'wb').write(r.content)

                    # keep track of simplified name
                    re_i['file_new_stem'] = finam2

            # get meta-data as df from jsom 
            _ = [a.pop('sono') for a in recs]
            df = pd.DataFrame(recs)
            df_all = df_all.append(df)

    if params_download:
        df_all.to_csv(   os.path.join(main_download_path, timstamp + '_meta.csv') )
        df_all.to_pickle(os.path.join(main_download_path, timstamp + '_meta.pkl') )



    # print summary 
    if params_download:
        print('Files that were downloaded:')
    else:
        print('Files to be downloaded:')    

    df_all['full_spec_name'] = df_all['gen'] + ' ' +  df_all['sp']
    print(pd.crosstab(df_all['full_spec_name'], df_all['cnt'], margins=True, dropna=False))
    print("")
    print(pd.crosstab(df_all['full_spec_name'], df_all['q'], margins=True, dropna=False))
    print("")
    print(df_all['lic'].value_counts())
    print("")








def xco_m2w():
    """   
    Convert mp3 to wav, this is a wrapper around ffmpeg.
    Looks for files ending in .mp3 throught all dirs inside ./downloads/ 
    and attempt to convert them to wav with ffmpeg
    """

    # parse CLI arguments
    if cli_call:
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('-ar', '--samplingrate', type=int , help='Required, sampling rate (int)')
        args = parser.parse_args()
        params_fs = args.samplingrate
    else: # devel 
        params_fs = 24000
        print(params_fs)

    # get list of all dirs inside './downloads/'
    all_d_dirs = next(os.walk(os.path.join(start_path, 'downloads')))[1]

    for pa in all_d_dirs:
        # process_path should contain mp3s, a wav_fs_ subdir will be created inside 
        process_path = os.path.join(start_path, 'downloads', pa) 

        destin_path = os.path.join(process_path, 'wav' + '_fs_' + str(params_fs) )
        if not os.path.exists(destin_path):
            os.mkdir(destin_path)

        all_mp3s = [a for a in os.listdir(process_path) if '.mp3' in a]

        for finam in all_mp3s:
            patin = os.path.join(process_path, finam)
            paout = os.path.join(destin_path, finam.replace('.mp3','.wav' ))

            # only convert if wav file does not yet exist 
            if not os.path.exists(paout):

                # convert mp3 to wav by call to ffmpeg
                try:
                    subprocess.call(['ffmpeg', 
                        '-y', # overwrite 
                        '-i', patin, 
                        '-ar', str(params_fs), 
                        '-ac', '1', # stereo to mono, take left channel
                        paout
                        ])
                except:
                    print("An exception occured!")


# 'ffmpeg', 
# '-i' # infile must be specifitd after -i
# -ar rate            set audio sampling rate (in Hz)
# -ac channels        set number of audio channels







# <<<<<<<<<<<<<<<<
# paaa = '/home/serge/sz_main/ml/data/xc_spec_03/downloads/download_20211016T222727/wav_fs_24000/Corvus_corax_XC439091_180810_1082_Aubrac_grand_corbeau.wav'
# data, fs = sf.read(paaa)
# data.shape

#-----------------
# make some noize 


def add_noise(fi, painp, paout, noize_fac = 0.1):
    """Load a wav file, add noise and save as wav"""
    assert(painp != paout), "painp and paout cannot be the same!"
    # load wav
    data, fs = sf.read(os.path.join(painp, fi))
    # add noize 
    noiz_std = noize_fac*data.std()
    noiz = np.random.normal(loc=0.0, scale=noiz_std, size=data.shape[0])
    data = data + noiz
    # Write   
    sf.write(os.path.join(paout, fi), data, fs)



if False: 
    all_wavs = os.listdir(destin_path)
    all_wavs = [a for a in all_wavs if '.wav' in a]
    for finam in all_wavs:
        print(destin_path + finam)
        add_noise(finam, destin_path, destin_path_noiz, noize_fac = 0.05)
















def xco_make_param():
    """  """
    dl_params = {
        "min_duration_s" : 5,
        "max_duration_s" : 15,
        "quality" : ["A", "B"],
        "exclude_nd" : True,
        "country" :[
            "Switzerland",
            "Mexico",
            "Australia"
            ],      
        "species" :[
            "Corvus corax", 
            "Corvus sinaloae",
            "Corvus coronoides"
            ]
        }

    with open(os.path.join(start_path, 'example.json'), 'w') as f:
        json.dump(dl_params, f,  indent=4)
