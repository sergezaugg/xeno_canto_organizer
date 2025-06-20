# Xeno-Canto Organizer (XCO)

## Summary
[Xeno-Canto (XC)](https://www.xeno-canto.org/) is a data treasure for ecology and bio-acoustics applications. 
However, the mp3 files cannot be directly used for machine learning (ML). 
**Xeno-Canto Organizer** is a Python toolkit to prepare Xeno-Canto bio-acoustic audio files **specifically for machine learning projects**

## Features
- Explicit selection of mp3 duration, quality, country, species gives fine control of what is included
- Summarize and filter files based on metadata prior to download.
- Convert MP3 files to WAV format and convert sampling rate (requires ffmpeg).
- Segment into pieces with custom duration and overlap
- Generate spectrograms that are stored as PNG images for easy exploration and ingestion by established CNNs
- Spectrogram parameters can be flexibly adjusted
- Stores the XC meta-data in PKL files that are easy to integrate with Python
- The complete download and preparation process can be handled (and replicated) with a small python script

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/xeno-canto-organizer.git
    cd xeno-canto-organizer
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # or 
    pip install -r req_mini.txt
    ```

3. **Install [ffmpeg](https://ffmpeg.org/) for audio conversion (if not already installed).**

## Project Structure

```
main.py                  # Demo script
xco.py                   # Main XCO class and functionality
spec/                    # Example scripts for various datasets
sample_json/             # Example parameter files
requirements.txt         # Dependencies
config.yaml              # Optional configuration
```

## Usage
1. Open **main.py** and set the a **start_path**, see sample code below. 
2. Make a template JSON to define the download, see sample code. 
3. Edit the JSON according to your needs (species, countries, recording duration and quality)
4. Run **main.py** line-by-line, check the files that are generated, adjust the parameters of your data preparation. 
5. Once **main.py** is ready, run all.
6. Result: metadata, mp3, wav, and spectrograms should be ready in their respective directories.
7. :satisfied: :smirk: Now you can throw your PyTorch magics at those PNGs (not covered in this codebase :wink:) 

### Sample code
Example of how preparation of data for an ML project can be handled with super-short Python script
```python
#----------------------
# minimalistic example
import os
import xco 
# make a projects dir, if it does not already exist
if not os.path.isdir('./temp_xc_project'):
    os.makedirs('./temp_xc_project')
# Make an instance of the XCO class and define the start path 
xc = xco.XCO(start_path = './temp_xc_project')
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

## Useful links
* https://creativecommons.org/licenses/
* https://xeno-canto.org/explore/api

## Limitation
* Apparently, only 1 country and 1 species per request allowed by XC API
* Only 1 request per second allowed by XC API

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements
- [xeno-canto.org](https://www.xeno-canto.org/) for providing open-access bird sound data.

## Author
- Created by [Serge Zaugg](https://www.linkedin.com/in/dkifh34rtn345eb5fhrthdbgf45/).




