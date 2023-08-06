#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import gevent
from gevent import monkey
monkey.patch_all()
import sys
import signal
from multiprocessing import Process
from public import configure
from worker import MonitorWorker, WarningWorker


prefix_pubsub_dict = {}


def how_to_use():
    print "usage: filter.py monitor.conf warning.conf"
    exit(-1)


def filter_func(monitor_conf, warning_conf):
    ppid = os.getppid()
    try:
        monitors = configure.get_monitors(monitor_conf)
        warnings = configure.get_warnings(warning_conf)
        mw_list = []
        ww_list = []
        for m in monitors:
            mw_list.append(MonitorWorker(m, prefix_pubsub_dict))
        for w in warnings:
            ww_list.append(WarningWorker(w, prefix_pubsub_dict))

        jobs = [
            gevent.spawn(mw.work) for mw in mw_list
        ] + [
            gevent.spawn(ww.work) for ww in ww_list
        ]
        gevent.joinall(jobs)
    finally:
        os.kill(ppid, signal.SIGABRT)


def gather_func(monitor_conf):
    ppid = os.getppid()
    try:
        gather_dir = "skygather"
        subprocess.call([gather_dir, monitor_conf])
    finally:
        os.kill(ppid, signal.SIGABRT)


def main():
    if len(sys.argv) > 3:
        how_to_use()
    if len(sys.argv) != 3:
        monitor_conf = "conf/monitor.conf"
        warning_conf = "conf/warning.conf"
    else:
        monitor_conf = sys.argv[1]
        warning_conf = sys.argv[2]

    p_gather = Process(target=gather_func, args=(monitor_conf, ))
    p_filter = Process(target=filter_func, args=(monitor_conf, warning_conf))

    p_gather.start()
    p_filter.start()
    # TODO
    # if any of this two threads quit, alert the warning and quit the whole program
    p_gather.join()
    p_filter.join()


if __name__ == "__main__":
    main()
