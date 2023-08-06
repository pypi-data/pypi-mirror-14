#!/usr/bin/env python
# coding: utf-8

import sys
import subprocess
from public import configure, communicate


def watch_file(file_path, messenger):
    proc = subprocess.Popen(["tail", "--retry", "-F", file_path], stdout=subprocess.PIPE)
    while True:
        msg = proc.stdout.readline()
        messenger.send_message(msg)


def gather_func():
    if len(sys.argv) != 2:
        print "usage: python gather.py monitor.conf"
        exit(-1)

    monitor_conf = sys.argv[1]
    conf = configure.get_monitors(monitor_conf)
    # 一定会有
    messenger = communicate.MQSender(conf[0]["log_file_path"], mq_model_type=communicate.PUSH)
    watch_file(conf[0]["log_file_path"], messenger)


if __name__ == "__main__":
    gather_func()
