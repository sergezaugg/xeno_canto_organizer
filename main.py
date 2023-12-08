"""
Created 20231203
Author: Serge Zaugg
"""

import xco 
import os 

# define root path 
xc = xco.XCO(start_path = os.path.join('C:\\Users\\sezau\\Desktop\\project01'))
# check stuff 
xc.XC_API_URL
xc.start_path
 
# create a example json parameter file, and edit it if you want.
xc.make_param()

# get summary of what would be downloaded
xc.get(params_json = 'example.json', params_download = False)

# download mp3 files into a timestamped directory and store the metadata with the same timestamp
xc.get(params_json = 'example.json', params_download = True)

# convert mp3s to wav with a specific sampling rate (wrapper to ffmpeg)
xc.mp3_to_wav(dir_tag = "20231208T090151", params_fs = 24000)

# extract spectrograms 
xc.extract_spectrograms(dir_tag = "20231208T090151", target_sampl_freq = 24000, duratSec = 5, win_siz = 1024, win_olap = 512, seg_step_size = 0.5, colormap = 'viridis')

# get summary table of all mp3 files 
xc.summary(save_csv = True)











# dev 


from torchvision.io import read_image
from torchvision.models import resnet50, ResNet50_Weights
import torch
# from PIL import Image
import numpy as np
# from torchvision import models
from torchsummary import summary
import gc

# Step 1: Initialize model with the best available weights
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.eval()
summary(model, (3, 224, 224))

# Step 2: Initialize the inference transforms
preprocess = weights.transforms()





pa = os.path.join('C:\\Users\\sezau\\Desktop\\project01', 'downloads', '20231208T090151_img_24000sps')

# first load all images 
imgs = []
for fi in [a for a in os.listdir(pa) if ".png" in a]:
    fi_fullpa = os.path.join(pa, fi)
    print(fi_fullpa)
    # fupa.append(fi_fullpa)
    img = read_image(fi_fullpa)
    type(img)
    imgs.append(img)


# predict by batches 
batch_size = 32
feature_vect = []
for i in np.arange(0,len(imgs), batch_size):
    print(i)
    # predict a batch of images 
    img_batch = imgs[(i):(i+batch_size)]
    imgs_arr = np.array(img_batch)
    imgs_arr = torch.from_numpy(imgs_arr)
    batch = preprocess(imgs_arr)
    feature_vect_i = model(batch)
    del(batch, imgs_arr, img_batch)
    gc.collect()
    print(feature_vect_i.shape)
    # convert to numpy as copy 
    feat_arr = feature_vect_i.cpu().detach().numpy() 
    feature_vect.append(feat_arr)
    del(feat_arr)
    gc.collect()


len(feature_vect)
feature_mat = np.concatenate(feature_vect)
feature_mat.shape



















# # only one image 
# img.dtype

# # Step 3: Apply inference preprocessing transforms
# batch = preprocess(img).unsqueeze(0)
# batch.size()
# batch.dtyp
# # Step 4: Use the model and print the predicted category
# prediction = model(batch).squeeze(0)


# prediction.shape









