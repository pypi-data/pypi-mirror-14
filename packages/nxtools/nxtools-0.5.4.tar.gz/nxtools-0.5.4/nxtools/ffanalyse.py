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

from __future__ import print_function

import re
import subprocess

from .logging import *
from .common import decode_if_py3

__all__ = ["ffanalyse"]


class FFAnalyse():
    def __init__(self, input_path, start=False, duration=False):
        self.proc = None
        self.cmd = ["ffmpeg", "-y"]
        if start:
            self.cmd.extend(["-ss", str(start)])
        self.cmd.extend(["-i", input_path])
        if duration:
            self.cmd.extend(["-t", str(duration)])
        afilters = "silencedetect=n=-20dB:d=5,ebur128,volumedetect"
        vfilters = "idet"
        for p in [
                ["filter:a", afilters],
                ["filter:v", vfilters],
                ["f", "null"]
                ]:
            self.cmd.extend(self.make_profile(p))
        self.cmd.append("-")
        self.reset_stderr()

    def reset_stderr(self):
        self.buff = self.error_log = ""

    @staticmethod
    def make_profile(p):
        cmd = []
        if type(p) == list and len(p) == 2:
            key, val = p
        elif type(p) == list:
            key = p[0]
            val = False
        else:
            key = p
            val = False
        cmd.append("-{}".format(key))
        if val:
            cmd.append(str(val))
        return cmd

    @property
    def is_running(self):
        return bool(self.proc) and self.proc.poll() == None

    @property
    def stdin(self):
        return self.proc.stdin

    @property
    def stderr(self):
        return self.proc.stderr

    @property
    def return_code(self):
        return self.proc.returncode

    def work(self, progress_handler=None):
        self.reset_stderr()
        result = {}
        tags = [
            ("mean_volume:", "audio/gain/mean"),
            ("max_volume:",  "audio/gain/peak"),
            ("I:",           "audio/r128/i"),
            ("Threshold:",   "audio/r128/t"),
            ("LRA:",         "audio/r128/lra"),
            ("Threshold:",   "audio/r128/lra/t"),
            ("LRA low:",     "audio/r128/lra/l"),
            ("LRA high:",    "audio/r128/lra/r"),
            ]
        logging.debug("Executing", " ".join(self.cmd))
        self.proc = subprocess.Popen(self.cmd, stderr=subprocess.PIPE)
        silences = []
        buff = ""
        exp_tag = tags.pop(0)
        last_idet = ""
        while self.is_running:
            ch = decode_if_py3(self.proc.stderr.read(1))
            if ch in ["\n", "\r"]:
                line = buff.strip()

                if line.startswith("[Parsed_ebur128"):
                    pass

                elif line.startswith("frame="):
                    m = re.match(r".*frame=\s*(\d+)\s*fps.*", line)
                    if m and progress_handler:
                        progress_handler(int(m.group(1)))

                elif line.find("silence_end") > -1:
                    m = re.match(r".*silence_end:\s*(\d+\.?\d*).*silence_duration:\s*(\d+\.?\d*).*", line)
                    if m:
                        e = float(m.group(1))
                        s = max(0, e - float(m.group(2)))
                        silences.append([s, e])

                elif line.find("Repeated Fields") > -1:
                    last_idet = line

                elif line.find(exp_tag[0]) > -1:
                    value = float(line.split()[-2])
                    result[exp_tag[1]] =  value
                    try:
                        exp_tag = tags.pop(0)
                    except:
                        break

                else:
                    self.error_log += buff + "\n"
                buff = ""
            else:
                buff += ch

        if silences:
            result["qc/silence"] = silences

        if last_idet:
            exp = r".*Repeated Fields: Neither:\s*(\d+)\s*Top:\s*(\d+)\s*Bottom:\s*(\d+).*"
            m = re.match(exp, last_idet)
            if m:
                n = int(m.group(1))
                t = int(m.group(2))
                b = int(m.group(3))
                tot = n + t + b
                if n / float(tot) < .9:
                    result["video/is_interlaced"] = True
        return result



def ffanalyse(input_path, start=False, duration=False, progress_handler=None):
    ff = FFAnalyse(input_path, start=start, duration=duration)
    return ff.work(progress_handler=progress_handler)


