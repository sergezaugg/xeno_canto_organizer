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
xc.extract_spectrograms(dir_tag = "20231208T090151", target_sampl_freq = 24000, duratSec = 1, win_siz = 64, win_olap = 32, seg_step_size = 1.0, colormap = 'viridis')

# get summary table of all mp3 files 
xc.summary(save_csv = True)











# dev 
from torchvision.io import read_image
# from torchvision.models import resnet50, ResNet50_Weights
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

import torch
import numpy as np
from torchsummary import summary
import gc
import re 
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import shutil
import os


# Step 1: Initialize model with the best available weights
# weights = ResNet50_Weights.DEFAULT
# model = resnet50(weights=weights)

weights = EfficientNet_B0_Weights.DEFAULT 
model = efficientnet_b0(weights=weights)

model.eval()
summary(model, (3, 5, 64))
# (129, 374)
# Step 2: Initialize the inference transforms
preprocess = weights.transforms()




################################
# FEATURE EXTRACTION
pa = os.path.join('C:\\Users\\sezau\\Desktop\\project01', 'downloads', '20231208T090151_img_24000sps')

# first load all images 
imgs = []
for fi in [a for a in os.listdir(pa) if ".png" in a]:
    fi_fullpa = os.path.join(pa, fi)
    print(fi_fullpa)
    # fupa.append(fi_fullpa)
    img = read_image(fi_fullpa)
    type(img)
    imgs.append([fi, img])

len(imgs)

# predict by batches 
batch_size = 32
feature_vect = []
finle_name_li = []
for i in np.arange(0,len(imgs), batch_size):
    print(i)
    # predict a batch of images 
    img_li = imgs[(i):(i+batch_size)]
    # extract file name
    finam_li = [a[0] for a in img_li]
    finle_name_li.extend(finam_li)
    # extract features 
    img_batch = [a[1] for a in img_li]
    imgs_arr = np.array(img_batch)
    imgs_arr.shape
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

# post process 
feature_mat = np.concatenate(feature_vect)
finle_name_arr = np.array(finle_name_li)


# feature_mat.shape
# finle_name_arr.shape
# feature_mat.max()
# feature_mat.min()





################################
# AGGLOM CLUSTERING

# clustering 
clu = AgglomerativeClustering(n_clusters=35, metric='euclidean', linkage='ward')

# clustering = clu.fit(feature_mat)
cluster_ids = clu.fit_predict(feature_mat)
cluster_ids.shape
pd.Series(cluster_ids).value_counts()

df = pd.DataFrame({
    'file_name' :finle_name_arr,
    'cluster_id' :cluster_ids,
    })

df['newname'] = df['cluster_id'].astype(str).str.cat(others=df['file_name'], sep='_')

# df['file_name'][3]
path_clusters = os.path.join(os.path.dirname(pa), 'clusters')
if not os.path.exists(path_clusters):
    os.mkdir(path_clusters)

for i,r in df.iterrows():
    print(r)

    path_cli=  os.path.join(path_clusters, str(r['cluster_id']))
    if not os.path.exists(path_cli):
        os.mkdir(path_cli)

    src = os.path.join(pa, r['file_name'])
    dst = os.path.join(path_cli, r['newname'])
    shutil.copy(src, dst)
















# # only one image 
# img.dtype
# # Step 3: Apply inference preprocessing transforms
# batch = preprocess(img).unsqueeze(0)
# batch.size()
# batch.dtyp
# # Step 4: Use the model and print the predicted category
# prediction = model(batch).squeeze(0)
# prediction.shape






# # get meta data from filename
# segm_index = float(re.split('_segm_', fi, maxsplit=10, flags=0)[1][0:3])
# str_temp = re.split('_', fi, maxsplit=10, flags=0)
# spec_names = str_temp[0]+ '_' + str_temp[1]
# xc_id = str_temp[2]


# pd.DataFrame([{
#     'fi' : fi,
#     'spec_names' : spec_names,
#     'xc_id' : xc_id,
#     'segm_index' : segm_index,
#     }])



