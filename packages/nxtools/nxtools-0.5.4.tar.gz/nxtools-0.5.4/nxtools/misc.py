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

import string

from .common import *

try:
    import unidecode
except:
    has_unidecode = False
else:
    has_unidecode = True

if PYTHON_VERSION < 3:
    import unicodedata


__all__ = ["indent", "unaccent", "slugify", "string2color", "fract2float"]


def indent(src, l=4):
    return "\n".join(["{}{}".format(l*" ", s.rstrip()) for s in src.split("\n")])


def unaccent(string, encoding="utf-8"):
    if has_unidecode:
        return unidecode.unidecode(string)
    if PYTHON_VERSION < 3:
        if type(string) == str:
            string = unicode(string, encoding)
        nfkd_form = unicodedata.normalize('NFKD', string)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).encode("ascii", "ignore")
    else:
        return string #TODO


def slugify(input_string, separator="-"):
    # TODO: fixme
    input_string = unaccent(input_string).lower()
    input_string = input_string.replace(" ", separator)
    input_string = "".join(ch for ch in input_string if ch in string.letters + string.digits + "-")
    return input_string


def string2color(string):
    h = 0
    for char in string:
        h = ord(char) + ((h << 5) - h)
    return hex(h & 0x00FFFFFF)


def fract2float(fract):
    nd = fract.split("/")
    try:
        if len(nd) == 1 or nd[1] == "1":
            return float(nd[0])
        return float(nd[0]) / float(nd[1])
    except:
        return 1
