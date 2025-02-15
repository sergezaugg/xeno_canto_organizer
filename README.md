# Xeno-Canto organizer
**A python class to download and organize Xeno-Canto audio files for machine learning projects.**

* Xeno-Canto (`https://www.xeno-canto.org/`) is a data treasure. 
* But the raw mp3 files cannot be directly used in machine learning processes (feature extraction, train, test) because they first need to be prepared. 
* This tool allows to download and organise XC data in a structured repository tree that can be directly accesed by your ML processes. 

## Summary
* check summaries before download (e.g. typos in species name, licences)
* lightweight meta-data format easy to postprocess with python
* explicit selection of mp3 file duration and licence
* Spectrogram parameters can be flexibly set, eg. very short spectrograms can be taken
* nested dirs with basic conversion (mp3 tp wav)
* spectrogram stored png which allows easy exploration

## Illustration

Snapshot of a few spectrograms saved as PNG obtained with this tool.

This is an illustration with some particular parameter values

* Mp3 were converted to wav files with fs=24000
* Wav files were cut into short pieces of 0.5 seconds and spectrograms extracted via short time Fourier transform (STFT)
* In this example, STFT window had 256 bins (Hamming) with 128 bins overlap
* Spectrograms were equalized (maad.sound.median_equalizer), log10 transformed and mapped to [0, 255]
* This gave small image with perfectly constant dimension 92 time bins x 129 frequency bins
* Original filename and position in original wav file is tracked in the filename
* For each file the Xc metadata is tracked in downloaded_data_meta.pkl

![](./images/spectros_01.png)  

## Why save spectrogram of sounds as PNG images ?
* Yes, for people working in acoustics it is a bit irritating
* It is handy because many PyTorch models and data augmentation procedures can directly ingest PNGs
* It is handy because images  can  be easily visualize with standard software
* Export as binary numpy files is planned but not yet available.


## Dependencies and installation
* Developed under Python 3.12.8
* Install ffmpg (see for example https://ffmpeg.org)
* Make a fresh venv and install the python packages 
```
pip install -r requirements.txt
```

## Usage
1. Make sure ffmpg and the python packages mentioned above are installed 
2. check in **config.yaml** that the url to xeno-canto API is still valid
3. Open **main.py** and run line-by-line at first to adjust the parameters
4. Once **main.py** is ready, run **main.py**
5. Result : metadata, mp3, wav, and spectrograms should be ready in their respective directories


















