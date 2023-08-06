# -*- coding: utf-8 -*-
#
#  zhuyin_table.py
#  cjktools
#

"""
An interface to the zhuyin <-> pinyin table.
"""

from functools import partial

from . import cjkdata
from cjktools.common import get_stream_context, stream_codec


def _default_stream():
    return open(cjkdata.get_resource('tables/zhuyin_pinyin_conv_table'))

_get_stream_context = partial(get_stream_context, _default_stream)


def parse_lines(istream):
    istream = stream_codec(istream)

    for line in istream:
        if not line.startswith('#'):
            yield line.rstrip().split()


def zhuyin_to_pinyin_table(istream=None):
    """ Returns a dictionary mapping zhuyin to pinyin. """
    with _get_stream_context(istream) as stream:
        table = {}
        for zhuyin, pinyin in parse_lines(stream):
            table[zhuyin] = pinyin

    return table


def pinyin_to_zhuyin_table(istream=None):
    """ Returns a dictionary mapping zhuyin to pinyin. """
    with _get_stream_context(istream) as istream:
        table = {}
        for zhuyin, pinyin in parse_lines(istream):
            table[pinyin] = zhuyin

    return table


def get_all_pinyin(istream=None):
    """ Returns a list of all pinyin """
    with _get_stream_context(istream) as istream:
        all_pinyin = ['r']

        for zhuyin, pinyin in parse_lines(istream):
            all_pinyin.append(pinyin)

    return all_pinyin


def pinyin_regex_pattern(istream=None):
    """ Returns a pinyin regex pattern, with optional tone number. """
    all_pinyin = get_all_pinyin(istream)

    # Sort from longest to shortest, so as to make maximum matches whenever
    # possible.
    all_pinyin = sorted(all_pinyin, key=len, reverse=True)

    # Build a generic pattern for a single pinyin with an optional tone.
    pattern = '(%s)([0-5]?)' % '|'.join(all_pinyin)

    return pattern


def zhuyin_regex_pattern(istream=None):
    """ Returns a zhuyin regex pattern. """
    with _get_stream_context(istream) as istream:
        all_pinyin = []

        for zhuyin, pinyin in parse_lines(istream):
            all_pinyin.append(pinyin)

    pattern = '(%s)[0-4]?' % '|'.join(all_pinyin)

    return pattern
