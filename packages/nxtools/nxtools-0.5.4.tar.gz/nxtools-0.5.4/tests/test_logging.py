#!/usr/bin/env python

from __future__ import print_function

from nxtools import *

print ()

logging.debug("Debug message")
logging.info("Info  message with different user", user="John Doe")
logging.warning("Warning! Warning!")
logging.goodnews("Good news, everyone!")

try:
    1/0
except:
    log_traceback("Traceback test")
