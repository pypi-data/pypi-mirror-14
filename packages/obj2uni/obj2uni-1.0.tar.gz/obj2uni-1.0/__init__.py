"""
Copyright (c) 2016 Mail.Ru Group LLC.


Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys

PY2 = sys.version_info[0] == 2

if not PY2:
    from functools import reduce


class objcmp(object):
    """
    Universal object comparison proxy.
    """
    def __init__(self, obj, *_):
        self.obj = obj

    def __lt__(self, other):
        try:
            return self.obj < other.obj
        except TypeError:
            return type(self.obj).__qualname__ < type(other.obj).__qualname__

    def __gt__(self, other):
        try:
            return self.obj > other.obj
        except TypeError:
            return type(self.obj).__qualname__ > type(other.obj).__qualname__

    def __eq__(self, other):
        try:
            return self.obj == other.obj
        except TypeError:
            return False

    def __le__(self, other):
        try:
            return self.obj <= other.obj
        except TypeError:
            return self < other

    def __ge__(self, other):
        try:
            return self.obj >= other.obj
        except TypeError:
            return self > other

    def __ne__(self, other):
        try:
            return self.obj != other.obj
        except TypeError:
            return True


def obj2uni(*seqs, **kwargs):
    """
    Maps each sequence from seqs to unicode strings with characters within
    range 0 - 0x10FFFF (0 - 0xFFFF on narrow Python 2.x builds - those
    not configured with --enable-unicode=ucs4).
    :param seqs: The sequences of arbitrary objects to map.
    :param mapping Existing character mapping to use, default is None (build
    it).
    :return: tuple <mapped strings>, <character to object mapping>
    """
    mapping = kwargs.get("mapping")
    if mapping is None:
        allobjs = reduce(set.union, map(set, seqs))
        uchr = chr if not PY2 else unichr
        try:
            uchr(0x100000)
            maxlen = 0x110000
        except ValueError:
            maxlen = 0x10000
        if len(allobjs) > maxlen:
            raise ValueError("Too large number of distinct objects (%d), "
                             "maximum is %d" % (len(allobjs), maxlen))
        mapping = {obj: uchr(i) for i, obj
                   in enumerate(sorted(allobjs, key=objcmp))}
        inv_mapping = {char: obj for obj, char in mapping.items()}
    else:
        inv_mapping = mapping
        mapping = {obj: char for char, obj in mapping.items()}
    mapped = tuple("".join(mapping[obj] for obj in seq) for seq in seqs)
    return mapped, inv_mapping
