#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='')

# Required positional argument
parser.add_argument('pos_arg', type=str, help='required, parameter file name (.json), can include relative path')

# Optional argument
parser.add_argument('-d', '--download', action='store_true', help='set -d to download files, else only a summary will be returned')

args = parser.parse_args()

print("Argument values:")
print(args.pos_arg)
print(args.download)

# $ ./papa.py aaa.json -d 
# $ ./papa.py /xxxx.json -d 


# /home/serge/sz_main/ml/src/xeno_canto_organizer

