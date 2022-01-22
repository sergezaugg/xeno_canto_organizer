"""
Created on Sat Apr 25 17:01:53 2020
@author: serge.zaugg
"""

import numpy as np
import scipy.signal as sgn 
import numpy as np
import wave
import struct

def funReadWavSegment(f, startSec, duratSec, fs, nChann, sampwidth):
    # f = wavFileName

    waveFile = wave.open(f, 'r')
    waveFile.setpos(int(fs*startSec)) 
    Nread = int(fs*duratSec)
    sigByte = waveFile.readframes(Nread) #read the all the samples from the file into a byte string
    waveFile.close()
    
    # convert bytes to a np-array 
    # struct.unpack(fmt, string)
    # h : int16 signed
    # H : int16 unsigned
    # i : int32 signed
    # I : int32 unsigned
    if sampwidth == 2 :
        unpstr = '<{0}h'.format(Nread*nChann) # < = little-endian h = 2 bytes ,16-bit 
    else:
        raise ValueError("Not a 16 bit signed interger audio formats.")
    
    sig = (struct.unpack(unpstr, sigByte)) # convert the byte string into a list of ints
    sig = np.array(sig, dtype=float)
    
    # convert from int to float
    sig = sig / ((2**(sampwidth*8))/2)
    
    return(sig)


def extract_dnn_input(sig, fs, win_siz, win_olap, mel_basis):
    """
    transform a segment of waveform to a normalized mel spectrogram 
    that can be fed into a DNN
    """
    
    # FEX
    sig = sig - sig.mean() # de-mean
    
    # compute spectrogram
    _, _, Xstft = sgn.spectrogram(x = sig, 
        fs = fs, 
        window = 'hamming', 
        nperseg = win_siz, 
        noverlap = win_olap, 
        detrend = 'constant', 
        return_onesided = True, 
        scaling = 'spectrum', 
        mode = 'psd')
    
    Xstft = Xstft.transpose()
    Xstft = np.log10(Xstft)
        
    # EQUALIZE
    nTimeBins = Xstft.shape[0]  
    nFreqBins = Xstft.shape[1]
    mystftMea = np.median(Xstft, axis=0) 
    mystftMea = np.broadcast_to(array = mystftMea, shape = (nTimeBins, nFreqBins))
    Xstft = np.subtract(Xstft, mystftMea)
    
    # MEL
    Xmel = np.matmul(Xstft, mel_basis.T )
    X = Xmel.astype('float32') 
    
    # SCALE
    X = (X - X.mean()) / X.std()

    # add a dummy dim - needed for Conv-2D
    X = np.expand_dims(X, 0)
    X = np.expand_dims(X, 3)
    
    # prepare for tf lite
    X = X.astype('float32')
    
    return(X)  




