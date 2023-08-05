#!/usr/bin/env python

from __future__ import print_function
import time

from nxtools import *

profile = [
        ["c:v", "copy"],
        ["c:a", "copy"],
        ["bsf:a", "aac_adtstoasc"]
        ]

ff = FFMPEG("http://tranquility.immstudios.org/nxtv.m3u8", "/home/martas/test.mp4", profile)
ff.start()
start_time = time.time()

while ff.is_running:
    elapsed_time = time.time() - start_time
    ff.process(progress_handler=lambda x: print ("at frame", x,  "elapsed", int(elapsed_time)))

    if elapsed_time > 60:
        ff.stop()
        break

print ("\n"*6)

