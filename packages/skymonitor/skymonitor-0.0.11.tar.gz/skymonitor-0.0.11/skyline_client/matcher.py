#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function # noqa
import sys
import re
from public import configure


def color_print(str, bg, fg):
    bg_s = bg[0]
    bg_e = bg[1]
    fg_s = fg[0]
    fg_e = fg[1]
    for i in xrange(len(str)):
        if i == bg_s:
            print('\033[0;0;43m', end="")
        if i == fg_s:
            print('\033[0;31;43m', end="")
        if i == fg_e:
            print('\033[0;0;43m', end="")
        if i == bg_e:
            print('\033[0m', end="")
        print(str[i], end="")
    print('\033[0m', end="")


def do_match(match_str, pattern_obj):
    match_obj = pattern_obj.search(match_str)
    if not match_obj:
        print(match_str)
        return
    if not match_obj.groups():
        print("here")
        color_print(match_str,
                    [match_obj.start(0), match_obj.end(0)],
                    [len(match_str) + 1, len(match_str) + 1])
    else:
        color_print(match_str,
                    [match_obj.start(0), match_obj.end(0)],
                    [match_obj.start(1), match_obj.end(1)])


def main():
    if len(sys.argv) < 3:
        print("usage: matcher.py monitor_conf_path match_file")
        exit(0)
    conf_path = sys.argv[1]
    match_file_path = sys.argv[2]
    try:
        conf = configure.get_monitors(conf_path)[0]
    except:
        print("%s configure file illeagal" % conf_path)
        exit(1)
    match_str = conf["match_str"]
    pattern_obj = re.compile(match_str)

    with open(match_file_path) as f:
        for l in f.readlines():
            do_match(l, pattern_obj)


if __name__ == "__main__":
    main()
