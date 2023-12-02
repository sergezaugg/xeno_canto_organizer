
import numpy as np
import scipy.signal as sgn 
import numpy as np
import wave
import struct

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






