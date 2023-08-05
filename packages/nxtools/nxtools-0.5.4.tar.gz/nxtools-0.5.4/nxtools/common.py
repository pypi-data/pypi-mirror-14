# The MIT License (MIT)
#
# Copyright (c) 2015 imm studios, z.s.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import sys

__all__ = ["decode_if_py3", "encode_if_py3", "PLATFORM", "PYTHON_VERSION", "find_binary"]

if sys.version_info[:2] >= (3, 0):
    PYTHON_VERSION = 3
    decode_if_py3 = lambda x: x.decode("utf-8")
    encode_if_py3 = lambda x: bytes(x, "utf-8")
else:
    PYTHON_VERSION = 2
    decode_if_py3 = lambda x: x
    encode_if_py3 = lambda x: x

PLATFORM = "windows" if sys.platform == "win32" else "unix"

def find_binary(fname):
    if PLATFORM == "unix":
        return fname
    elif PLATFORM == "windows":
        if not fname.endswith(".exe"):
            fname = fname + ".exe"
        for p in sys.path:
            c = os.path.join(p, fname)
            if os.path.exists(c):
                return c
