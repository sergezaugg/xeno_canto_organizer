# -------------
# Author : Serge Zaugg
# Description : Main functionality of this codebase
# -------------

import os
import re
import json
import requests
import pandas as pd
import unidecode
import numpy as np 
import wave
import scipy.signal as sgn 
import matplotlib.pyplot as plt  
from PIL import Image
import struct
from maad import sound
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
        """
        Description : Convert 'mm:ss' (str) to seconds (int)
        """
        x = x.split(':')
        x = int(x[0])*60 + int(x[1])
        return(x)
    

    def _clean_xc_filenames(self, s):
        """
        Description : keep only alphanumeric characters in a strin and remove '.mp3'
        """
        stri = s.replace('.mp3', '')
        stri = unidecode.unidecode(stri)
        stri = stri.replace(' ', '_').replace('-', '_')
        stri = re.sub(r'[^a-zA-Z0-9_]', '', stri)
        return(stri)
    
    # _clean_xc_filenames(s = "öüä%&/sdf__caca_.55&/())äöüöä5.mp3")


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

    def make_param(self, filename = 'download_params.json', template = "mini"):
        """ 
        Description: Create a template download parameters file 
        Arguments:
            filename: (str), file name ending in .json
            template: (str), which template to use. Valid values are "mini", "n_europe", "sw_europe"
        Returns: Writes a json file to disc
        """
        if template == "mini":
            with open(os.path.join('./sample_json/xc_downl_mini.json')) as f:
                dl_params = json.load(f)
        elif template == "n_europe":
            with open(os.path.join('./sample_json/xc_downl_n_europe.json')) as f:
                dl_params = json.load(f)
        elif template == "sw_europe":
            with open(os.path.join('./sample_json/xc_downl_sw_europe.json')) as f:
                dl_params = json.load(f)    
        elif template == "sw_europe_small":
            with open(os.path.join('./sample_json/xc_downl_sw_eur_small.json')) as f:
                dl_params = json.load(f)    
        else:
            return("Please provide a valid value for argument 'template'")
    
        with open(os.path.join(self.start_path, filename), 'w') as f:
            json.dump(dl_params, f,  indent=4)


    def get_summary(self, params_json):
        """ 
        Description: Prepares a list of file to be downloaded, the list includes XC metadata
        Arguments:   params_json (str) : Path to a json file (templates json can be created by XCO.make_param())
        Returns:     df_recs (data frame) : A dataframe listing the files to be downloaded
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
                print(full_query_string)
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
                if len(recs) <= 0:
                    continue
                recs_pool.extend(recs)
        # make df and return
        df_recs = pd.DataFrame(recs_pool)
        df_recs['full_spec_name'] = df_recs['gen'] + ' ' +  df_recs['sp']
        return(df_recs)


    def download(self, df_recs):
        """ 
        Description : Downloads mp3 files from XCO.XC_API_URL and stores them in XCO.start_path
        Arguments : df_recs (data frame) : A dataframe returned by XCO.get_summary()
        Returns: Files are written to XCO.start_path; nothing is returned into Python session
        """
        # Create directory to where files will be downloaded
        source_path = os.path.join(self.start_path, self.download_tag + '_orig')
        if not os.path.exists(source_path):
            os.mkdir(source_path)
        # download one file for each row
        new_filename = []
        for i,row_i in df_recs.iterrows():
            re_i = row_i.to_dict()
            print("Downloading file: ", re_i["file-name"])
            full_download_string = re_i["file"]
            # actually download files 
            rq = requests.get(full_download_string, allow_redirects=True)
            # simplify and clean filename
            finam2 = self._clean_xc_filenames(s = re_i["file-name"])
            # add genus and species into filename
            finam2 = re_i['gen'] + "_" + re_i['sp'] + '_' + finam2
             # write file to disc
            open(os.path.join(source_path, finam2 + '.mp3') , 'wb').write(rq.content)
            new_filename.append(finam2)
            # row_i['finam2'] = finam2
        # print(new_filename)
        df_all_extended = df_recs
        df_all_extended['file_name_stub'] = new_filename 
        df_all_extended['full_spec_name'] = df_all_extended['gen'] + ' ' +  df_all_extended['sp']
        df_all_extended.to_pickle(os.path.join(self.start_path, self.download_tag + '_meta.pkl') )

    

    def mp3_to_wav(self, target_fs):
            """   
            Description : Looks for files ending in .mp3 and attempt to convert them to wav with ffmpeg
            Arguments :   target_fs : the sampling rate of the saved wav file  
            Returns:      Writes wav files to disc
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



    def extract_spectrograms(self, target_fs, segm_duration, segm_step = 1.0, win_siz = 256, win_olap = 128,  equalize = True, colormap = 'gray', eps = 1e-10):
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
                waveFile.close()

                # make sure fs is correct 
                if myFs != target_fs:
                    print("Wav file ignored because its sampling frequency is not equal to target_fs !  " + wavFileName)
                    continue
                print("Processing file: " + wavFileName)
                
                # loop over segments within file   
                totNbSegments = int(totDurFile_s / segm_duration)  
                for ii in np.arange(0, (totNbSegments - 0.99), segm_step):
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
                        # transpose, equalize and log-transform 
                        X = np.flip(X, axis=0) # so that high freqs at top of image 
                        if equalize:
                            X = sound.median_equalizer(X) # equalize 
                        X = np.log10(X + eps)
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
                        # image_save_path = os.path.join(path_destin, os.path.basename(wavFileName).replace('.wav','_segm_') + str(ii) + ".png")
                        startSec_str = "{:005.3f}".format(startSec).zfill(8) # make a fixed length string for start second
                        image_save_path = os.path.join(path_destin, os.path.basename(wavFileName).replace('.wav','_segm_') + str(startSec_str) + ".png")
                        im.save(image_save_path)
                    except:
                        print("Error during loop over segments of wav file!")
            except:
                print("Error while reading wav file!")

            
                


# devel code - supress execution if this is imported as module 
if __name__ == "__main__":
    print("Hi V, you passed beyond the blackwall, you are in the dev space now!")

    plt.colormaps()
    


 