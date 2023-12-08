"""
Created 20231203
Author: Serge Zaugg
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
import wave
import pickle
import scipy.signal as sgn 
import matplotlib.pyplot as plt  
import numpy as np
from PIL import Image
import struct
import numpy as np
# from skimage import filters
# import maad  
from  maad import sound


def read_piece_of_wav(f, start_sec, durat_sec, fs, n_ch, sampwidth):
    """ 
    f = wav file name 
    """
    # read wav 
    wave_file = wave.open(f, 'r')
    wave_file.setpos(int(fs*start_sec)) 
    Nread = int(fs*durat_sec)
    sig_byte = wave_file.readframes(Nread) #read the all the samples from the file into a byte string
    wave_file.close()
    # convert bytes to a np-array 
    # struct.unpack(fmt, string)
    # h : int16 signed
    # H : int16 unsigned
    # i : int32 signed
    # I : int32 unsigned
    if sampwidth == 2 :
        unpstr = '<{0}h'.format(Nread*n_ch) # < = little-endian h = 2 bytes ,16-bit 
    else:
        raise ValueError("Not a 16 bit signed interger audio formats.")
    # convert byte string into a list of ints
    sig = (struct.unpack(unpstr, sig_byte)) 
    sig = np.array(sig, dtype=float)
    # convert from int to float
    sig = sig / ((2**(sampwidth*8))/2)
    # return 
    return(sig)



class XCO():

    def __init__(self, start_path):
        self.XC_API_URL = 'https://www.xeno-canto.org/api/2/recordings'
        self.start_path = start_path # '/home/serge/sz_main/ml/data/xc_dev'

    # helper functions 
    def __convsec(self, x):
        """Convert 'mm:ss' (str) to seconds (int)"""
        x = x.split(':')
        x = int(x[0])*60 + int(x[1])
        return(x)

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


    def summary(self, save_csv = True):
        # import all pkl with an append all dfs and export as csv
        main_download_path = os.path.join(self.start_path, 'downloads')
        # main_download_path = os.path.join('C:\\Users\\sezau\\Desktop\\data2', 'downloads')

        all_pkls = [a for a in os.listdir(main_download_path) if '_meta.pkl' in a]

        df_summ_li = []
        for a in all_pkls:
            df_summ_li.append(pd.read_pickle(os.path.join(main_download_path, a))) 
          
            # print(len(df_summ_li))
        df_summary = pd.concat(df_summ_li)
        df_summary.sort_values(by=['gen','sp','cnt','q'], axis=0, ascending=True, inplace=True, ignore_index=True)

        # check if full path points to an existing file 
        all_files = df_summary['downloaded_to_path'] + '/' + df_summary['downloaded_to_file_stem'] + '.mp3'
        df_summary['file_exists']  = [os.path.exists(p) for p in all_files]
        # save as csv 
        timstamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')   
    
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
        if save_csv:
            df_summa.to_csv(os.path.join(self.start_path, 'summary_agg_' + timstamp + '.csv') )
            df_summary.to_csv(   os.path.join(self.start_path, 'summary_' + timstamp + '.csv') )
        else:
            return(df_summary)




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
                # print(recs)
                self.recs = recs
                if len(recs) > 0:
                    for l in range(len(recs)):
                        # print(recs[l]['rmk'])
                        recs[l]["also"] = ' + '.join(recs[l]["also"])
                        for k in recs[l].keys():
                            # print(recs[l][k])
                            try:
                                recs[l][k] = recs[l][k].replace(';', '')
                            except:
                                3+3
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
                print("Downloading files ...")
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



    def mp3_to_wav(self, dir_tag, params_fs):
        """   
        Convert mp3 to wav, this is a wrapper around ffmpeg.
        Looks for files ending in .mp3 and attempt to convert them to wav with ffmpeg
        """
        self.dir_tag = dir_tag
        self.params_fs = params_fs
        # 
        all_dirs = next(os.walk(os.path.join(self.start_path, 'downloads')))[1]
        thedir = [a for a in all_dirs if "_orig" in a and self.dir_tag in a][0]
        path_source = os.path.join(self.start_path, 'downloads', thedir)
        path_destin = os.path.join(self.start_path, 'downloads', thedir.replace('_orig','_wav_' + str(self.params_fs) + 'sps'))
        if not os.path.exists(path_destin):
            os.mkdir(path_destin)
        all_mp3s = [a for a in os.listdir(path_source) if "mp3" in a]

        for finam in all_mp3s:
            print(finam)
            patin = os.path.join(path_source, finam)
            paout = os.path.join(path_destin, finam.replace('.mp3','.wav' ))
            # only convert if wav file does not yet exist 
            if not os.path.exists(paout):
                # convert mp3 to wav by call to ffmpeg
                try:
                    subprocess.call(['ffmpeg', 
                        '-y', # -y overwrite without asking 
                        '-i', patin, # '-i' # infile must be specifitd after -i
                        '-ar', str(self.params_fs), # -ar rate set audio sampling rate (in Hz)
                        '-ac', '1', # stereo to mono, take left channel # -ac channels set number of audio channels
                        paout
                        ])
                except:
                    print("An exception occured!")



    





    def extract_spectrograms(self, dir_tag, target_sampl_freq, duratSec, win_siz, win_olap, seg_step_size = 1.0, colormap = 'viridis'):
        """
        # plt.col ormaps()
        # 'viridis' 'inferno'  'magma'  'inferno'  'plasma'  'twilight'
        """

        #-------------------------------- 
        all_dirs = next(os.walk(os.path.join(self.start_path, 'downloads')))[1]
        thedir = [a for a in all_dirs if "_wav_" in a and dir_tag in a]
        thedir = [a for a in thedir if str(target_sampl_freq) in a ][0]
        path_source = os.path.join(self.start_path, 'downloads', thedir)
        path_destin = os.path.join(self.start_path, 'downloads', thedir.replace('_wav_','_img_'))
        if not os.path.exists(path_destin):
            os.mkdir(path_destin)
        all_wavs = [a for a in os.listdir(path_source) if "wav" in a]
        allWavFileNames = [os.path.join(path_source, a) for a in all_wavs]

        #-------------------------------- 
        params_dict = {
            "sampling_frequency" : target_sampl_freq,
            "segment_duration_sec" : duratSec,
            "segment_step_size" : seg_step_size,
            "fft_window_size_bins" : win_siz,
            "fft_window_overlap_bins" : win_olap,
            "colormap" : colormap,
            }
        
        with open(os.path.join(path_destin, "feature_extraction_parameters.pkl"), 'wb') as f:
            pickle.dump(params_dict, f)

        # loop over wav files 
        for wavFileName in  allWavFileNames:  
                
            # open wav file and get meta-information 
            waveFile = wave.open(wavFileName, 'r')
            myFs = waveFile.getframerate()
            totNsam = waveFile.getnframes()
            totDurFile_s = totNsam / myFs
            nchannels = waveFile.getnchannels()    
            sampwidth = waveFile.getsampwidth()
            waveFile.close()
            
            # make sure fs is correct 
            if myFs != target_sampl_freq:
                print("myFs not equal to target_sampl_freq !!!")
                continue
            
            totNbSegments = int(totDurFile_s / duratSec)

            # loop over segments within file     
            for ii in  np.arange(0, (totNbSegments - 0.99), seg_step_size)   :
                print(ii)
                startSec = ii*duratSec
                sig = read_piece_of_wav(f = wavFileName, start_sec = startSec, durat_sec = duratSec, fs = myFs, n_ch = nchannels, sampwidth = sampwidth)
                # de-mean
                sig = sig - sig.mean() 
                # compute spectrogram
                _, _, X = sgn.spectrogram(x = sig, 
                    fs = myFs, 
                    window = 'hamming', 
                    nperseg = win_siz, 
                    noverlap = win_olap, 
                    detrend = 'constant', 
                    return_onesided = True, 
                    scaling = 'spectrum', 
                    mode = 'psd')
                # transpose and log 
                X = np.flip(X, axis=0) # so that hifg freqs at to of image 

                # equalize 
                X = sound.median_equalizer(X) 

                X = X.transpose()
                X = np.log10(X)

                # save image as PNG 
                arr = X.T
                # normalize 
                arr = arr - arr.min()
                arr = arr/arr.max()
                # color map             
                map_val = colormap
                cm = plt.get_cmap(map_val)
                colored_image = cm(arr)
                im = Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8))
                # save as image 
                image_save_path = os.path.join(path_destin, os.path.basename(wavFileName).replace('.wav','_segm_') + str(ii) + ".png")
                im.save(image_save_path)

              









# from skimage import filters
# import maad  
# from  maad import sound

# print(">>>>>>>>>>>", X.shape)
# X = sound.median_equalizer(X)
# print(">>>>>>>>>>>", X.shape)


# # new 
# X_mea = filters.gaussian(X, sigma=45, mode='nearest', cval=0, preserve_range=False, truncate=4.0)
# X = X - X_mea




