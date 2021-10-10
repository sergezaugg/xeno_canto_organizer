#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 23:03:36 2021
@author: serge
"""

import requests
import pandas as pd
import re
import unidecode

n_files_per_spec = 3

source_path = '/home/serge/sz_main/ml/data/xc_spec_03/'

# helper 
def convsec(x):
    x = x.split(':')
    x = int(x[0])*60 + int(x[1])
    return(x)




bird_species = { 
    'Attila bolivianus': 'dull_capped_attila_song', 
    'Amazona festiva': 'festive_amazon_call', 
    # 'Cacicus cela': 's000040',
    # 'Capito aurovirens': 's000015',
    # 'Crotophaga major': 's000031',
    # 'Crypturellus undulatus': 'undulated_tinamou_song', 
    # 'Glaucidium brasilianum': 's000014',
    # 'Leptotila rufaxilla': 'grayfronted_dove_song', 
    # 'Monasa nigrifrons': 'black_fronted_nunbird_song',
    # 'Myrmelastes hyperythrus': 's000010', 
    # 'Nasica longirostris': 'updownsweep_2kHz_dur1s_01',
    # 'Nyctibius grandis': 's000003', 
    # 'Nyctibius griseus' : 's000021',
    # 'Psarocolius angustifrons': 's000020', 
    # 'Pitangus sulphuratus': 's000038',
    # 'Ramphastos tucanus': 's000025',
    # 'Taraba major': 's000022', 
    # 'Trogon melanurus': 's000016',
    # 'Xiphorhynchus guttatus': 's000011',
    # 'Xiphorhynchus obsoletus': 's000023', 
    }


len(bird_species)
bird_species.keys()

df_all = pd.DataFrame()
for ke, va in bird_species.items():
    print(ke, va)
    
    search_str = ke.replace(' ', '+') 
    tag = search_str.replace('+','_') + '_'
     
    url = 'https://www.xeno-canto.org/api/2/recordings?query=' + search_str
    r = requests.get(url, allow_redirects=True)
    j = r.json()
#    print (json.dumps(j, sort_keys=True, indent=4))
    recs = j['recordings']

    print(search_str + ' ' + str(len(recs)))
    recs = [a for a in recs if convsec(a["length"]) > 10 and convsec(a["length"]) <= 600] 
    # excude files with no-derivative licenses
    recs = [a for a in recs if not 'nd' in a['lic']]
    recs = [a for a in recs if not 'ND' in a['lic']]
    recs = [a for a in recs if 'A' in a['q'] or 'B' in a['q'] or 'C' in a['q']]
    # take first n
    recs = recs[0:n_files_per_spec]
    print(search_str + ' ' + str(len(recs)))
    print('')

    # download 
    for re_i in recs:
        print(len(re_i["also"]))
        re_i["also"] = ' + '.join(re_i["also"])
        print(re_i["file"])
        length_s = convsec(re_i["length"])
        url = 'http:' + re_i["file"]
        r = requests.get(url, allow_redirects=True)
        # simplify filename stem 
        finam2 = re_i["file-name"].replace('.mp3', '')
        finam2 = unidecode.unidecode(finam2)
        finam2 = finam2.replace(' ', '_').replace('-', '_')
        finam2 = re.sub(r'[^a-zA-Z0-9_]', '', finam2)
        finam2 = tag + finam2
#        open(source_path + tag + finam2 + '_' + str(length_s) + '.mp3', 'wb').write(r.content)
        open(source_path  + finam2 + '.mp3', 'wb').write(r.content)
        # keep track simplified name
        re_i['file_new_stem'] = finam2
        re_i['sound_type'] = va

    # get meta-data as df from jsom 
    [a.pop('sono') for a in recs]
    df = pd.DataFrame(recs)
    df_all = df_all.append(df)

df_all.to_csv(source_path + '_meta_all_' + '_meta.csv')
df_all.to_pickle(source_path + '_meta_all_' + '_meta.pkl')

print(df_all['gen'].value_counts())

## --------------
#CC BY
#CC BY-SA 
#CC BY-ND # cannot be edited 
#CC BY-NC
#CC BY-NC-SA 
#CC BY-NC-ND # cannot be edited 

#search_str = 'nr:388556'
# search_str = 'Attila+bolivianus'

