#!/usr/bin/env python
# coding: utf-8

import sys
from public import configure, communicate


def gather_func():
    if len(sys.argv) != 2:
        print "usage: python gather.py monitor.conf"
        exit(-1)

    monitor_conf = sys.argv[1]
    conf = configure.get_monitors(monitor_conf)
    # 一定会有
    pub_sub = communicate.MQSender(conf[0]["log_file_path"], mq_model_type=communicate.PUSH)
    file_watch = configure.FileWatcher(conf[0], pub_sub)
    file_watch.start_loop()


if __name__ == "__main__":
    gather_func()
