"""
Created 20211010
@author: serge Zaugg
"""

import os
import re
import json
import requests

import pandas as pd
import unidecode
import datetime 
import subprocess
import numpy as np 
import soundfile as sf




class XCO():

    def __init__(self):
        self.XC_API_URL = 'https://www.xeno-canto.org/api/2/recordings'
        self.start_path = '/home/serge/sz_main/ml/data/xc_dev'

    # helper functions 
    def __convsec(self, x):
        """Convert 'mm:ss' (str) to seconds (int)"""
        x = x.split(':')
        x = int(x[0])*60 + int(x[1])
        return(x)

    def __add_some_noise(self, painp, paout, noize_fac = 0.1):
        """Load a wav file, add noise and save as wav"""
        assert(painp != paout), "painp and paout cannot be the same!"
        # load wav
        data, fs = sf.read(painp)
        # add noize 
        noiz_std = noize_fac*data.std()
        noiz = np.random.normal(loc=0.0, scale=noiz_std, size=data.shape[0])
        data = data + noiz
        # Write   
        sf.write(paout, data, fs)


    def make_param(self):
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

        with open(os.path.join(self.start_path, 'example.json'), 'w') as f:
            json.dump(dl_params, f,  indent=4)


    def summary(self):
        # import all pkl with an append all dfs and export as csv
        main_download_path = os.path.join(self.start_path, 'downloads')

        all_pkls = [a for a in os.listdir(main_download_path) if '_meta.pkl' in a]

        df_summary = pd.DataFrame()
        for a in all_pkls:
            df_summary = df_summary.append(pd.read_pickle(os.path.join(main_download_path, a))) 

        df_summary.sort_values(by=['gen','sp','cnt','q'], axis=0, ascending=True, inplace=True, ignore_index=True)

        # check if full path points to an existing file 
        all_files = df_summary['downloaded_to_path'] + '/' + df_summary['downloaded_to_file_stem'] + '.mp3'
        df_summary['file_exists']  = [os.path.exists(p) for p in all_files]
        # save as csv 
        timstamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')   
        df_summary.to_csv(   os.path.join(self.start_path, 'summary_' + timstamp + '.csv') )

        # make per-species aggregated summaries 
        df_summary['length_sec'] =  df_summary['length'].apply(self.__convsec) # get total length
        df01 = pd.crosstab(df_summary['full_spec_name'], df_summary['cnt'], margins=True, dropna=False)
        df02 = pd.crosstab(df_summary['full_spec_name'], df_summary['q'], margins=True, dropna=False)
        df03 = pd.DataFrame(df_summary.groupby('full_spec_name')['length_sec'].sum())
        # merge 
        df_summa = df01
        df_summa = df_summa.merge(df02, how = "outer", on = ['full_spec_name'])
        df_summa = df_summa.merge(df03, how = "outer", on = ['full_spec_name'])
        df_summa.reset_index(inplace=True)
        # save to disc
        df_summa.to_csv(os.path.join(self.start_path, 'summary_agg_' + timstamp + '.csv') )





    # main function to download mp3 from XC, or just get a summary
    def get(self, params_json, params_download = False):

        main_download_path = os.path.join(self.start_path, 'downloads')

        if not os.path.exists(main_download_path):
            os.mkdir(main_download_path)

        # get all metadata from already downloaded files 
        pkls_li = [a for a  in os.listdir(main_download_path) if a.endswith('_meta.pkl')]
        df_meta = []
        if len(pkls_li) > 0:
            df_meta = pd.concat( [pd.read_pickle(os.path.join(main_download_path,a)) for a in pkls_li] )
            df_meta = df_meta['id'].tolist()



        # load parameters from json file 
        with open(os.path.join(self.start_path, params_json)) as f:
            dl_params = json.load(f)



        # retrieve meta data from XC web and select candidate files to be downloaded
        print("") 
        print("*******************************") 
        print("Retrieving meta-data from xc and apply selection filters ...")
        n_excl = 0
        recs_pool = []
        for cnt in dl_params['country']:
            cnt_str = '+cnt:' + cnt
            for ke in dl_params['species']:        
                search_str = ke.replace(' ', '+') 
                # API HTTP request of meta data 
                full_query_string = self.XC_API_URL + '?query=' + search_str + cnt_str
                r = requests.get(full_query_string, allow_redirects=True)
                j = r.json()
                recs = j['recordings']
                # exclude if length not in specified range 
                recs = [a for a in recs if self.__convsec(a["length"]) > dl_params['min_duration_s'] and self.__convsec(a["length"]) <= dl_params['max_duration_s']]
                # exclude files with no-derivative licenses
                if dl_params['exclude_nd']:
                    recs = [a for a in recs if not 'nd' in a['lic'].lower()]
                # select based on quality rating of recordings
                recs = [a for a in recs if a['q'] in dl_params['quality']]
                # exclude recordings that were already downloaded             
                before_exclusion = len(recs)
                recs = [a for a in recs if a['id'] not in df_meta]
                n_excluded = before_exclusion - len(recs)
                n_excl += n_excluded
                # get meta-data as df from jsom 
                _ = [a.pop('sono') for a in recs]

                # replace "";"" by empty string in all values (needed for later export as csv)
                if len(recs) > 0:
                    for l in range(len(recs)):
                        # print(recs[l]['rmk'])
                        recs[l]["also"] = ' + '.join(recs[l]["also"])
                        for k in recs[l].keys():
                            recs[l][k] = recs[l][k].replace(';', '')
                        # print(recs[l]['rmk'])

                recs_pool.extend(recs)

            

            # recs_pool[6]['rmk']

        # final handling
        print(n_excl, 'of the selected files available locally ...')
        if (n_excl>0): print( "... they will not be downloaded again")
        print("There are " + str(len(recs_pool)) + " files for download after applying the selection filters")
        
        if len(recs_pool) > 0:
            df_all = pd.DataFrame(recs_pool)
            if params_download:
                print("Writing meta-information to pkl ...") 
                # Create time-stamped directory where files will be downloaded
                timstamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')   
                source_path = os.path.join(main_download_path, timstamp + '_orig')
                if not os.path.exists(source_path):
                    os.mkdir(source_path)
                # make a copy of parameter file and meta information
                with open(os.path.join(main_download_path, timstamp + '_params.json'), 'w') as fp:
                    json.dump(dl_params, fp,  indent=4)
    
                # download 
                print("Downloading wav files ...")
                for re_i in recs_pool:
                    # re_i["also"] = ' + '.join(re_i["also"])
                    # full_download_string = 'http:' + re_i["file"]
                    full_download_string = re_i["file"]
                    # actually download files 
                    r = requests.get(full_download_string, allow_redirects=True)
                    # simplify filename stem 
                    finam2 = re_i["file-name"].replace('.mp3', '')
                    finam2 = unidecode.unidecode(finam2)
                    finam2 = finam2.replace(' ', '_').replace('-', '_')
                    finam2 = re.sub(r'[^a-zA-Z0-9_]', '', finam2)
                    tag =  re_i['gen'] + "_" + re_i['sp'] + '_'
                    finam2 = tag + finam2
                    # write file to disc
                    open(os.path.join(source_path, finam2 + '.mp3') , 'wb').write(r.content)
                    # keep track of simplified name
                    re_i['downloaded_to_path'] = source_path
                    re_i['downloaded_to_file_stem'] = finam2
                df_all_extended = pd.DataFrame(recs_pool)
                df_all_extended['full_spec_name'] = df_all_extended['gen'] + ' ' +  df_all_extended['sp']
                df_all_extended.to_csv(   os.path.join(main_download_path, timstamp + '_meta.csv') )
                df_all_extended.to_pickle(os.path.join(main_download_path, timstamp + '_meta.pkl') )
                
            print("")
            print("Details:")
            df_all['full_spec_name'] = df_all['gen'] + ' ' +  df_all['sp']
            print(pd.crosstab(df_all['full_spec_name'], df_all['cnt'], margins=True, dropna=False))
            print("")
            print(pd.crosstab(df_all['full_spec_name'], df_all['q'], margins=True, dropna=False))
            print("")
            print(df_all['lic'].value_counts())

        print("*******************************") 
        print("") 



    def m2w(self, params_fs = 48000):
        """   
        Convert mp3 to wav, this is a wrapper around ffmpeg.
        Looks for files ending in .mp3 throught all dirs inside ./downloads/ 
        and attempt to convert them to wav with ffmpeg
        """

        # get list of all dirs inside './downloads/'
        all_d_dirs = next(os.walk(os.path.join(self.start_path, 'downloads')))[1]
        all_d_dirs = [a for a in all_d_dirs if '_orig' in a]

        for pa in all_d_dirs:
            # process_path should contain mp3s, a wav_fs_ subdir will be created inside 
            process_path = os.path.join(self.start_path, 'downloads', pa) 

            destin_path = process_path.replace('_orig','') + '_wav_' + str(params_fs) + 'sps'
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
                            '-y', # -y overwrite without asking 
                            '-i', patin, # '-i' # infile must be specifitd after -i
                            '-ar', str(params_fs), # -ar rate set audio sampling rate (in Hz)
                            '-ac', '1', # stereo to mono, take left channel # -ac channels set number of audio channels
                            paout
                            ])
                    except:
                        print("An exception occured!")













    #-----------------
    # make some noize 

    def add_noise(self, params_fs, params_noize):
        """   
        Take all wav files with a given sampling rate and add acontrolled amount of white noise.
        """

        # get list of all relevant dirs inside './downloads/'
        all_d_dirs = next(os.walk(os.path.join(self.start_path, 'downloads')))[1]
        all_d_dirs = [a for a in all_d_dirs if '_wav_' in a]
        all_d_dirs = [a for a in all_d_dirs if str(params_fs) + 'sps' in a]

        for pa in all_d_dirs:
            # process_path should contain mp3s, a wav_fs_ subdir will be created inside 
            process_path = os.path.join(self.start_path, 'downloads', pa) 

            destin_path = process_path.replace('_wav','_noise') + '_n_' + str(params_noize) 
            if not os.path.exists(destin_path):
                os.mkdir(destin_path)

            all_wavs = [a for a in os.listdir(process_path) if '.wav' in a]

            for finam in all_wavs:
                patin = os.path.join(process_path, finam)
                paout = os.path.join(destin_path, finam)

                # only convert if wav file does not yet exist 
                if not os.path.exists(paout):
                    try:
                        self.__add_some_noise(patin, paout, noize_fac = params_noize)
                    except:
                        print("An exception occured!")









