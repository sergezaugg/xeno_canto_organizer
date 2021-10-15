"""
Created 20211010
@author: serge Zaugg
"""

import os
import json

def main():

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

