

# pip install pymp3

import mp3
from wave import Wave_write

patin = "C:/Users/sezau/Desktop/project01/downloads/20250104T110600_orig/Corvus_corax_XC356384_Raven.mp3"
paout = "C:/Users/sezau/Desktop/project01/downloads/20250104T110600_orig/zzz.wav"

with open(patin, 'rb') as read_file, open(paout, 'wb') as write_file:
    decoder = mp3.Decoder(read_file)
    sample_rate = decoder.get_sample_rate()
    nchannels = decoder.get_channels()
    wav_file = Wave_write(write_file)
    wav_file.setnchannels(nchannels)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    while True:
        pcm_data = decoder.read()
        # type(pcm_data)
        if not pcm_data:
            break
        else:
            wav_file.writeframes(pcm_data)





import wave
import struct
import numpy as np
import scipy.signal as sgn 
from scipy.io.wavfile import write

def wav_to_mono_convert_fs(f, f_out, fs_new):
    """ 
    read wave file f, convert to mono, re-sample and save a wave in f_out 
    """
    # read wav 
    wave_file = wave.open(f, 'r')
    n_ch = wave_file.getnchannels()
    print('n_ch', n_ch)
    sampwidth = wave_file.getsampwidth()
    print('orig fs', wave_file.getframerate())
    wave_file.setpos(int(0)) 
    Nread = int(wave_file.getnframes())
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
    # sig = sig / ((2**(sampwidth*8))/2)

    # take only first channel 
    sig = sig[0::n_ch]

    # resample to adjust fs
    sampling_rate = wave_file.getframerate()
    number_of_samples = round(len(sig) * float(fs_new) / sampling_rate)
    sig = sgn.resample(sig, number_of_samples)

    # signal as numpy integer array 
    sig = sig.astype('int16')
    # save to file in wav format
    write(filename = f_out, rate = fs_new, data = sig)
    # return 
    return("converted")

# 

pa_wav_in = "C:/Users/sezau/Desktop/project01/downloads/20250104T110600_orig/zzz.wav"
pa_wav_out = "C:/Users/sezau/Desktop/project01/downloads/20250104T110600_orig/zzz_002.wav"

wav_to_mono_convert_fs(f = pa_wav_in, f_out = pa_wav_out, fs_new = 4000)




# xs = np.array([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4])
# xs[0::1]



