# Xeno-Canto organizer 

**A python tool to prepare Xeno-Canto audio files for machine learning projects**

### Summary
* Xeno-Canto (XC) (https://www.xeno-canto.org) is a data treasure for ecology and bio-acoustics applications. 
* However, the mp3 files cannot be directly used for machine learning (ML). 
* This tool allows to download and prepare XC data for ML project.
* It is a single class with a few methods for download, conversion, data segmentation and spectrograms extraction.
* Thus, the complete download and preparation process can be handled in a small python script, see sample code below and **main.py**.
* All intermediate and final items are written to files in a single directory tree.
* :warning: Running the code can download many mp3 files :warning:

### Features
* Summaries can be checked before actual download
* Explicit selection of mp3 duration, quality, country, species gives fine control of what is included
* Also stores the XC meta-data in PKL files that are easy to integrate with Python
* Spectrogram parameters can be flexibly adjusted
* Spectrogram stored as PNG images for easy exploration and ingestion by established CNNs

### Usage
1. Download this repo as zip and initialize a new .git to track you personal changes in **main.py**.
2. Make sure **ffmpg** and Python packages are installed (see Dependencies and installation)
3. Open **main.py** and set the a **start_path**, see sample code below. 
4. Make a template JSON to define the download, see sample code. 
5. Edit the JSON according to your needs (species, countries, recording duration and quality)
6. Run **main.py** line-by-line, check the files that are generated, adjust the parameters of your data preparation. 
7. Once **main.py** is ready, run the complete **main.py**.
8. Result: metadata, mp3, wav, and spectrograms should be ready in their respective directories.
9. :satisfied: :smirk: Now you can throw your PyTorch magics at those PNGs (not covered in this codebase :wink:) 

### Sample code
Example of how preparation of data for an ML project can be handled with super-short Python script
```python
#----------------------
# minimalistic example
import xco 
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = 'C:/<path where data will be stored>')
# Create a template json parameter file (to be edited)
xc.make_param(filename = 'download_criteria.json', template = "mini")
# Get information of what will be downloaded
xc.download_summary(params_json = 'download_criteria.json')
# Make summaries  
print(xc.df_recs.shape)
# Download the files 
xc.download_audio_files()
# Convert mp3s to wav with a specific sampling rate (requires ffmpeg to be installed)
xc.mp3_to_wav(conversion_fs = 24000)
# Extract spectrograms from segments and store as PNG
xc.extract_spectrograms(fs_tag = 24000, segm_duration = 1.0, segm_step = 0.5, win_siz = 512, win_olap = 192, max_segm_per_file = 12, equalize = True, colormap='viridis')

```

## Illustration
* The figure below is a snapshot of a few spectrograms obtained with this tool
* MP3 were converted to wav files with a fixed sampling frequency
* Wav files were cut into pieces and spectrograms extracted 
* Spectrograms were equalized, log10-transformed and mapped to [0, 255]
* Can be exported as 1-channel or 3-channel images

![](./images/spectros_01.png)  


## Why save spectrogram of sounds as PNG images
* It is handy because many PyTorch models and data augmentation procedures can directly ingest PNGs
* It is handy because images can be easily visualized with standard software
* Yes, 3-channel is an overkill but easier to be ingested by Image CNNs such as ResNet and co

## Dependencies and installation
* Needs internet access to download data from the XC API https://www.xeno-canto.org/api/2/recordings
* Developed under Python 3.12.8
* Install **ffmpg** (see for example https://ffmpeg.org)
* Make a fresh venv and install the python packages with pip: 
```bash
pip install -r requirements.txt
```

## Hints
* Check in **config.yaml** that the url to XC API is still valid

## Useful links
* https://creativecommons.org/licenses/
* https://xeno-canto.org/explore/api

## Limitation
* Apparently, only 1 country and 1 species per request allowed by XC API
* Only 1 request per second allowed by XC API















