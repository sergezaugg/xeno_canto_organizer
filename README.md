# xcorganize
**A python-based command line tool to download and organize Xeno-Canto audio files for machine learning projects.**

Xeno canto is a data treasure.
But the data cannot be directly used in ML processes (feature extraction, train test) it first need to be organized.
This tool set allows to easily download and organise XC data in a local repository that can be directly accesd by your ML processes.  

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
# Make a empty directory where all your files and meta-data will be stored
mkdir xc_all_downloads 
# cd into it
cd xc_all_downloads
# create a template json parameter file
xco_make_param 
# get summary of what would be downloaded
xco_get dparam00.json
# download the mp3 files and the metadata
xco_get dparam00.json -d
# a time stamped directory was created and all file downloaded into it
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



