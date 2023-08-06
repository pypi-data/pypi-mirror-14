#!/usr/bin/env python
#! coding: utf-8

import sys
from public import configure, pubsub


def gather_func(monitor_conf):
    conf = configure.get_monitors(monitor_conf)
    # 一定会有
    pub_sub = pubsub.PubSub(conf[0]["log_file_path"])
    file_watch = configure.FileWatcher(conf[0], pub_sub)
    file_watch.start_loop()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "usage: python gather.py monitor.conf"
        exit(-1)

    conf_path = sys.argv[1]
    gather_func(conf_path)
