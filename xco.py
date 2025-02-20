# """
# Created 20231203
# Author : Serge Zaugg
# """

import os
import re
import json
import requests
import pandas as pd
import unidecode
import numpy as np 
import wave
import pickle
import scipy.signal as sgn 
import matplotlib.pyplot as plt  
from PIL import Image
import struct
from  maad import sound
import subprocess
import yaml

class XCO():

    #----------------------------------
    # (0) the init method

    def __init__(self, start_path):
        with open('./config.yaml') as f:
            conf = yaml.safe_load(f)
        self.XC_API_URL = conf['XC_API_URL']
        self.start_path = start_path 
        self.download_tag = 'downloaded_data'  

    #----------------------------------
    # (1) helper functions
    
    def _convsec(self, x):
        """Convert 'mm:ss' (str) to seconds (int)"""
        x = x.split(':')
        x = int(x[0])*60 + int(x[1])
        return(x)

    def _read_piece_of_wav(self, f, start_sec, durat_sec): 
        """ 
        Description : Reads a piece of a wav file 
        Arguments :
            f : (str), full path to a wav file 
            start_sec : (float), time location in seconds where the piece to be extracted starts
            durat_sec : (float), duration in seconds of the piece to be extracted 
        Returns: A 1D numpy-array (float) containing the extracted piece of the waveform  
        """
        # read wav 
        wave_file = wave.open(f, 'r')
        # extract metadata from wave file header
        fs = wave_file.getframerate()
        n_ch = wave_file.getnchannels()  
        sampwidth = wave_file.getsampwidth()
        # read bytes from the chunk of 
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
            raise ValueError("Not a 16 bit signed integer audio formats.")
        # convert byte string into a list of ints
        sig = (struct.unpack(unpstr, sig_byte)) 
        sig = np.array(sig, dtype=float)
        # convert from int to float
        sig = sig / ((2**(sampwidth*8))/2)
        # return 
        return(sig)


    #----------------------------------
    # (2) main methods 

    def make_param(self, filename = 'download_params.json'):
        """ 
        Description: Create a template download parameters file 
        Arguments:
            filename: (str), file name ending in .json
        Returns: Writes a json file to disc
        """
        dl_params = {
            "min_duration_s" : 5.5,
            "max_duration_s" : 6,
            "quality" : ["A", "B"],
            "exclude_nd" : True,
            "country" :[
                "Switzerland",
                "France"
                ],      
            "species" :[
                "Fringilla coelebs",
                "Cyanistes caeruleus"
                ]
            }
        with open(os.path.join(self.start_path, filename), 'w') as f:
            json.dump(dl_params, f,  indent=4)


    def get_summary(self, params_json):
        """ 
        get a summary
        """
        # load parameters from json file 
        with open(os.path.join(self.start_path, params_json)) as f:
            dl_params = json.load(f)

        # retrieve meta data from XC web and select candidate files to be downloaded
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
                recs = [a for a in recs if self._convsec(a["length"]) > dl_params['min_duration_s'] and self._convsec(a["length"]) <= dl_params['max_duration_s']]
                # exclude files with no-derivative licenses
                if dl_params['exclude_nd']:
                    recs = [a for a in recs if not 'nd' in a['lic'].lower()]
                # select based on quality rating of recordings
                recs = [a for a in recs if a['q'] in dl_params['quality']]
                # get meta-data as df from jsom 
                _ = [a.pop('sono') for a in recs]

                # replace "";"" by empty string in all values (needed for later export as csv)
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

        # final handling
        print("There are " + str(len(recs_pool)) + " files for download")
        if len(recs_pool) <= 0:
            return("selection criteria gave zero files to download")
        
        # if length of recs_pool is > 0
        df_all = pd.DataFrame(recs_pool)
        return(df_all, recs_pool)


    def download(self, recs_pool):

        main_download_path = os.path.join(self.start_path)
        if not os.path.exists(main_download_path):
            os.mkdir(main_download_path)

        print("Writing meta-information to pkl ...") 
        # Create directory to where files will be downloaded
        source_path = os.path.join(main_download_path, self.download_tag + '_orig')
        if not os.path.exists(source_path):
            os.mkdir(source_path)
    
        # download 
        print("Downloading files ...")
        for re_i in recs_pool:
            # re_i["also"] = ' + '.join(re_i["also"])
            # full_download_string = 'http:' + re_i["file"]
            full_download_string = re_i["file"]
            # actually download files 
            r = requests.get(full_download_string, allow_redirects=True)
            # simplify and clean filename stem 
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
        df_all_extended.to_csv(   os.path.join(main_download_path, self.download_tag + '_meta.csv') )
        df_all_extended.to_pickle(os.path.join(main_download_path, self.download_tag + '_meta.pkl') )

    

    def mp3_to_wav(self, target_fs):
            """   
            Description : Looks for files ending in .mp3 and attempt to convert them to wav with ffmpeg
            Arguments :
                target_fs : the sampling rate of the saved wav file  
            Returns: Writes wav files to disc
            """
            all_dirs = next(os.walk(os.path.join(self.start_path)))[1]
            thedir = [a for a in all_dirs if "_orig" in a and self.download_tag in a][0]
            path_source = os.path.join(self.start_path, thedir)
            path_destin = os.path.join(self.start_path, thedir.replace('_orig','_wav_' + str(target_fs) + 'sps'))
            if not os.path.exists(path_destin):
                os.mkdir(path_destin)
            all_mp3s = [a for a in os.listdir(path_source) if "mp3" in a]
            # loop over mp3 file and convert to wav by call to ffmpeg
            for finam in all_mp3s:
                # print(finam)
                patin = os.path.join(path_source, finam)
                paout = os.path.join(path_destin, finam.replace('.mp3','.wav' ))
                try:
                    subprocess.call(['ffmpeg', 
                        '-y', # -y overwrite without asking 
                        '-i', patin, # '-i' # infile must be specifitd after -i
                        '-ar', str(target_fs), # -ar rate set audio sampling rate (in Hz)
                        '-ac', '1', # stereo to mono, take left channel # -ac channels set number of audio channels
                        paout
                        ])
                except:
                    print("An exception occurred during mp3-to-wav conversion with ffmpeg!")



    def extract_spectrograms(self, target_fs, segm_duration, segm_step = 1.0, win_siz = 256, win_olap = 128,  equalize = True, colormap = 'gray'):
        """
        Description : Process wav file by segments, for each segment makes a spectrogram, and saves a PNG
        Arguments : 
            target_fs (float) : If wav with different fs are available, this will force to use only one fs.
            segm_duration (float) : Duration of a segment in seconds
            segm_step (float) : Overlap between consecutive segments, 1.0 = no overlap, 0.5 = 50% overlap
            win_siz (int) : Size in nb of bins of the FFT window used to compute the short-time fourier transform
            win_olap (int) : Size in nb of bins of the FFT window overlap
            equalize (Boolean) : Set True to apply equalization (suppresses stationary background noise), else set to False
            colormap (str) : 
                Set to 'gray' to write one-channel images (default)
                Other strings will map spectrogram to 3-channel color images e.g. 'viridis', 'inferno', 'magma', 'inferno', 'plasma', 'twilight' 
                For full list see see plt.colormaps()
        Returns : PNG images are saved to disc
        """

        assert win_olap < win_siz, "win_olap must be strictly smaller that win_siz"

        #-------------------------------- 
        all_dirs = next(os.walk(os.path.join(self.start_path)))[1]
        thedir = [a for a in all_dirs if "_wav_" in a and self.download_tag in a]
        thedir = [a for a in thedir if str(target_fs) in a ][0]
        path_source = os.path.join(self.start_path,  thedir)
        path_destin = os.path.join(self.start_path,  thedir.replace('_wav_','_img_'))
        if not os.path.exists(path_destin):
            os.mkdir(path_destin)
        all_wavs = [a for a in os.listdir(path_source) if "wav" in a]
        allWavFileNames = [os.path.join(path_source, a) for a in all_wavs]
        # print(allWavFileNames)

        # pragmatically get time and frequency axes 
        sig_rand = np.random.uniform(size=int(segm_duration*target_fs))   
        f_axe, t_axe, _ = sgn.spectrogram(x = sig_rand, fs = target_fs, nperseg = win_siz, noverlap = win_olap, return_onesided = True)
      
        # save parameters for later traceability
        params_dict = {
            "sampling_frequency" : target_fs,
            "segment_duration_sec" : segm_duration,
            "segment_step_size" : segm_step,
            "fft_window_size_bins" : win_siz,
            "fft_window_overlap_bins" : win_olap,
            "colormap" : colormap,
            "frequency_axis" : f_axe.tolist(),
            "time_axis" : t_axe.tolist(),
            }
        with open(os.path.join(path_destin, "feature_extraction_parameters.json"), 'w') as f:
            json.dump(params_dict, f, indent=4)    

        # loop over wav files 
        for wavFileName in allWavFileNames: 
            try:
                # open wav file and get meta-information 
                waveFile = wave.open(wavFileName, 'r')
                myFs = waveFile.getframerate()
                totNsam = waveFile.getnframes()
                totDurFile_s = totNsam / myFs
                nchannels = waveFile.getnchannels()    
                sampwidth = waveFile.getsampwidth()
                waveFile.close()

                # make sure fs is correct 
                if myFs != target_fs:
                    print("Wav file ignored because its sampling frequency is not equal to target_fs !  " + wavFileName)
                    continue
                print("Processing file: " + wavFileName)
                
                # loop over segments within file   
                totNbSegments = int(totDurFile_s / segm_duration)  
                for ii in  np.arange(0, (totNbSegments - 0.99), segm_step):
                    # print(ii)
                    try:
                        startSec = ii*segm_duration
                        sig = self._read_piece_of_wav(f = wavFileName, start_sec = startSec, durat_sec = segm_duration)
                        sig = sig - sig.mean() # de-mean
                        # compute spectrogram
                        f_axe, t_axe, X = sgn.spectrogram(
                            x = sig, 
                            fs = myFs, 
                            window = 'hamming', 
                            nperseg = win_siz, 
                            noverlap = win_olap, 
                            detrend = 'constant', 
                            return_onesided = True, 
                            scaling = 'spectrum', 
                            mode = 'psd')
                        # remove nyquist freq
                        X = X[:-1, :]
                        # transpose and log 
                        X = np.flip(X, axis=0) # so that high freqs at top of image 
                        if equalize:
                            X = sound.median_equalizer(X) # equalize 
                        X = np.log10(X)
                        # normalize 
                        X = X - X.min()
                        X = X/X.max()
                        # facultatively apply color map  
                        if colormap == "gray":
                            im = Image.fromarray((X[:, :] * 255).astype(np.uint8))
                        else:           
                            cm = plt.get_cmap(colormap)
                            colored_image = cm(X)
                            im = Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8))
                        # print("PIL image size: ", im.size, im.mode)
                        # save as image 
                        image_save_path = os.path.join(path_destin, os.path.basename(wavFileName).replace('.wav','_segm_') + str(ii) + ".png")
                        im.save(image_save_path)
                    except:
                        print("Error during loop over segments of wav file!")
            except:
                print("Error while reading wav file!")

            
                


# devel code - supress execution if this is imported as module 
if __name__ == "__main__":
    print("Hi V, you passed beyond the blackwall, you are in the dev space now!")

    plt.colormaps()
    
    xc = XCO(start_path = 'C:/temp_xc_projects/proj04')
    xc._convsec("44:55")

    wavFileName = "C:/temp_xc_projects/proj04/downloaded_data_wav_24000sps/Corvus_coronoides_XC620107_2021_01_17_Corvus_coronoides2.wav"
    # open wav file and get meta-information 
    waveFile = wave.open(wavFileName, 'r')
    myFs = waveFile.getframerate()
    totNsam = waveFile.getnframes()
    totDurFile_s = totNsam / myFs
    nchannels = waveFile.getnchannels()    
    sampwidth = waveFile.getsampwidth()
    waveFile.close()
    x_out = xc._read_piece_of_wav(
        f = wavFileName, 
        start_sec = 1.0, 
        durat_sec = 2.0, 
        )
    type(x_out)
    x_out.dtype

    # """ 
    # Description : aaa
    # Arguments : bbb
    # Returns : ccc
    # """


    sig_rand = np.random.uniform(size=int(78))  
    sig_rand.tolist()
