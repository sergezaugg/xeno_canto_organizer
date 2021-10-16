"""
Created 20211010
@author: serge Zaugg
"""

import os
import sys
import re
import json
import requests
import pandas as pd
import unidecode
import datetime 
import argparse

# constant parameters
XC_API_URL = 'https://www.xeno-canto.org/api/2/recordings'

# helper functions 
def convsec(x):
    """Convert 'mm:ss' (str) to seconds (int)"""
    x = x.split(':')
    x = int(x[0])*60 + int(x[1])
    return(x)




# main function to download mp3 from XC, or just get a summary
def xco_download():

    # evalutes to False in interactive mode and True in script mode 
    import __main__ as main_module
    cli_call = hasattr(main_module, '__file__')

    if cli_call:
        start_path = os.getcwd() # get dir from which script was called 
    else: # devel 
        start_path = '/home/serge/sz_main/ml/data/xc_spec_03' 

    main_download_path = os.path.join(start_path, 'downloads')

    if not os.path.exists(main_download_path):
        os.mkdir(main_download_path)




    # parse CLI arguments
    if cli_call:
        parser = argparse.ArgumentParser(description='')
        parser.add_argument('params_json', type=str, help='required, parameter file name (.json), can include relative path')
        parser.add_argument('-d', '--download', action='store_true', help='set -d to download files, else only a summary will be returned')
        args = parser.parse_args()
        params_json = args.params_json
        params_download = args.download
    else: # devel 
        params_json = "dparam00.json"
        params_download = False
        print(params_json)
        print(params_download)

 

    # load parameters from json file 
    with open(os.path.join(start_path, params_json)) as f:
        dl_params = json.load(f)

    bird_species = dl_params['species']
   

    if params_download:
        # Create time-stamped directory where files will be downloaded
        timstamp = 'download_' + datetime.datetime.now().strftime('%Y%m%dT%H%M%S')   
        source_path = os.path.join(main_download_path, timstamp)
        if not os.path.exists(source_path):
            os.mkdir(source_path)
        print("Retrieving info from xc and downloading ...")    
        # make a copy of parameter file
        with open(os.path.join(source_path, params_json), 'w') as fp:
            json.dump(dl_params, fp,  indent=4)
    else:
        print("retrieving info from xc ...")




    df_all = pd.DataFrame()
    for cnt in dl_params['country']:
        cnt_str = '+cnt:' + cnt

        for ke in dl_params['species']:        
            search_str = ke.replace(' ', '+') 
            tag = search_str.replace('+','_') + '_'
            
            full_query_string = XC_API_URL + '?query=' + search_str + cnt_str
            r = requests.get(full_query_string, allow_redirects=True)

            j = r.json()
            recs = j['recordings']

            # exclude if length no in specified range 
            recs = [a for a in recs if convsec(a["length"]) > dl_params['min_duration_s'] and convsec(a["length"]) <= dl_params['max_duration_s']]
            
            # excude files with no-derivative licenses
            recs = [a for a in recs if not 'nd' in a['lic']]
            recs = [a for a in recs if not 'ND' in a['lic']]

            # select based on quality rating of recordings
            recs = [a for a in recs if a['q'] in dl_params['quality']]

            len(recs)




            # download 
            if params_download:
                for re_i in recs:
                    # print(len(re_i["also"]))
                    re_i["also"] = ' + '.join(re_i["also"])
                    # print(re_i["file"])
                    length_s = convsec(re_i["length"])

                    full_download_string = 'http:' + re_i["file"]

                    r = requests.get(full_download_string, allow_redirects=True)

                    # simplify filename stem 
                    finam2 = re_i["file-name"].replace('.mp3', '')
                    finam2 = unidecode.unidecode(finam2)
                    finam2 = finam2.replace(' ', '_').replace('-', '_')
                    finam2 = re.sub(r'[^a-zA-Z0-9_]', '', finam2)
                    finam2 = tag + finam2

                    open(os.path.join(source_path, finam2 + '.mp3') , 'wb').write(r.content)

                    # keep track of simplified name
                    re_i['file_new_stem'] = finam2

            # get meta-data as df from jsom 
            [a.pop('sono') for a in recs]
            df = pd.DataFrame(recs)
            df_all = df_all.append(df)

    if params_download:
        df_all.to_csv(   os.path.join(main_download_path, timstamp + '_meta.csv') )
        df_all.to_pickle(os.path.join(main_download_path, timstamp + '_meta.pkl') )



    # print summary 
    if params_download:
        print('Files that were downloaded:')
    else:
        print('Files to be downloaded:')    

    df_all['full_spec_name'] = df_all['gen'] + ' ' +  df_all['sp']
    print(pd.crosstab(df_all['full_spec_name'], df_all['cnt'], margins=True))
    print("")
    print(pd.crosstab(df_all['full_spec_name'], df_all['q'], margins=True))
    print("")

















def xco_make_param():

    # evalutes to False in interactive mode and True in script mode 
    import __main__ as main_module
    cli_call = hasattr(main_module, '__file__')
    if cli_call:
        start_path = os.getcwd() # get dir from which script was called 
    else: # devel 
        start_path = '/home/serge/sz_main/ml/data/xc_spec_03' 

    dl_params = {
        "min_duration_s" : 10,
        "max_duration_s" : 15,
        "quality" : ["A", "B"],
        "country" :[
            "Brazil", 
            "Bolivia"
            ],      
        "species" :[
            "Attila bolivianus", 
            "Amazona festiva", 
            "Taraba major" 
            ]
        }

    with open(os.path.join(start_path, 'dparam00.json'), 'w') as fp:
        json.dump(dl_params, fp,  indent=4)
