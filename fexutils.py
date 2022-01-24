
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


def extract_spectrogram(sig, fs, win_siz, win_olap, mel_basis):
    """
    transform waveform to mel spectrogram 
    """
    # de-mean
    sig = sig - sig.mean() 
    # compute spectrogram
    _, _, X = sgn.spectrogram(x = sig, 
        fs = fs, 
        window = 'hamming', 
        nperseg = win_siz, 
        noverlap = win_olap, 
        detrend = 'constant', 
        return_onesided = True, 
        scaling = 'spectrum', 
        mode = 'psd')
    # transpose and log 
    X = X.transpose()
    X = np.log10(X)
    # equalize
    nTimeBins = X.shape[0]  
    nFreqBins = X.shape[1]
    mystftMea = np.median(X, axis=0) 
    mystftMea = np.broadcast_to(array = mystftMea, shape = (nTimeBins, nFreqBins))
    X = np.subtract(X, mystftMea)
    # mel
    X = np.matmul(X, mel_basis.T )
    X = X.astype('float32') 
    # scale
    X = (X - X.mean()) / X.std()
    # add a dummy dim
    X = np.expand_dims(X, 0)
    X = np.expand_dims(X, 3)
    # return
    return(X)  




