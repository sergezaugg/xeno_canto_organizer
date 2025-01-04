



import numpy as np
import gc
import re 
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import shutil
import os
from PIL import Image

from skimage.measure import block_reduce

# C:\Users\sezau\Desktop\proj2\downloaded_data_img_24000sps

################################
# FEATURE EXTRACTION
# pa = os.path.join('C:\\Users\\sezau\\Desktop\\proj2', 'downloaded_data_img_24000sps')
pa = os.path.join('C:\\Users\\sezau\\Desktop\\project01', 'downloaded_data_img_24000sps')


# first load all images 
imgs = []
for fi in [a for a in os.listdir(pa) if ".png" in a]:
    fi_fullpa = os.path.join(pa, fi)
    print(fi_fullpa)
    # fupa.append(fi_fullpa)
    img = Image.open(fi_fullpa).convert('L')
    img = np.array(img)
    type(img)
    img.shape
    imgs.append([fi, img])

len(imgs)
# [a[1].shape for a in imgs]
im_stack = np.array([a[1] for a in imgs])
im_stack.shape

# post process 
feature_mat_f   = im_stack.mean(axis=2)
feature_mat_t   = im_stack.mean(axis=1)

# reduce granularits of time features 
feature_mat_t.shape
feature_mat_t = block_reduce(feature_mat_t,(1,4), np.mean)
feature_mat_t.shape

feature_mat_f.shape
feature_mat_t.shape
feature_mat = np.concatenate([feature_mat_f, feature_mat_t], axis=1)

finle_name_arr = np.array([a[0] for a in imgs])


# feature_mat.shape
# finle_name_arr.shape
# feature_mat.max()
# feature_mat.min()






################################
# AGGLOM CLUSTERING

# clustering 
clu = AgglomerativeClustering(n_clusters=21, metric='euclidean', linkage='ward')

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



