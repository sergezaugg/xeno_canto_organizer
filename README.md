# xcorganize
**A python-based command line tool to download and organize Xeno-Canto audio files for machine learning projects.**

Xeno-Canto* is a data treasure. But the data cannot be directly used in machine learning processes (feature extraction, train, test) because it first need to be organized. This toolset allows to download and organise XC data in a structured repository tree that can be directly accesd by your ML processes. 
The tool is meant for incrementally adding consistently with previously used data. 


*`https://www.xeno-canto.org/`


## Summary
- check summaries before download (e.g. typos in species name, licences)
- incremetaly download more and more data 
- lightweigh meta-data format easy to postprocess with python
- explicit selection of duration and licence
- nested dirs with basic conversion (mp3 tp wav, resample, add noise to remove mp3 artefacts)
- rename files as pure alphanumeric

## Usage

- recomendation: Make a Python venv first 

- Linux or Windows Powershell
```bash

# Make a root directory where files and meta-data will be stored
mkdir xc_all_downloads 

# cd into it (all command should be calld forom the root dir)
cd xc_all_downloads

# create a example json parameter file, and edit it if you want.
xco_make_param 

# get summary of what would be downloaded
xco_get example.json

# add the -d flag to download mp3 files into a timestamped directory and store the metadata with the same timestamp
xco_get example.json -d

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xco_m2w -ar 48000

# add noise to wavs for a specific sampling rate 
xco_add_noise -ar 48000 -n 0.10

```



all command from xco will take the current dir as reference



## Installation

## prerequisites
ffmpg

## Python dependencies


# misc 
python -m pip install --upgrade pip setuptools wheel
python3 -m pip install --upgrade build

python -m build




## --------------
#CC BY
#CC BY-SA 
#CC BY-ND # cannot be edited 
#CC BY-NC
#CC BY-NC-SA 
#CC BY-NC-ND # cannot be edited 

#search_str = 'nr:388556'
# search_str = 'Attila+bolivianus'






Use the following general guidelines when rating recordings on xeno-canto. Ratings are obviously subjective, and will inevitably vary slightly between different individuals, but these guidelines should improve consistency.

    A: Loud and Clear
    B: Clear, but bird a bit distant, or some interference with other sound sources
    C: Moderately clear, or quite some interference
    D: Faint recording, or much interference
    E: Barely audible








ND clause (No Derivative) 


Attribution
CC BY

Attribution-ShareAlike
CC BY-SA 

Attribution-NoDerivs
CC BY-ND 

Attribution-NonCommercial
CC BY-NC 

Attribution-NonCommercial-ShareAlike
CC BY-NC-SA 

Attribution-NonCommercial-NoDerivs
CC BY-NC-ND 



