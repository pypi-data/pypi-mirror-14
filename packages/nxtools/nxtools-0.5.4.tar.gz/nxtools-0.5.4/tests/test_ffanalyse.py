#!/usr/bin/env python


import os
from themis import *
from nxtools import *

if __name__ == "__main__":
    input_dir = "/home/martas/temp/demo_clips/srce"
    output_dir = "/home/martas/temp/demo_clips/norm"

    for input_path in get_files(input_dir):
        print (ffanalyse(input_path))
