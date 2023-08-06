#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import sys
import signal
from multiprocessing import Process
from public import configure
from skyconf import DEBUG


PROCESS_NUM = 8


def how_to_use():
    print "usage: filter.py monitor.conf warning.conf"
    exit(-1)


def monitor_worker_func(monitor_conf, monitor_idx):
    ppid = os.getppid()
    try:
        if DEBUG:
            script_dir = "/home/liuweibo/skyline/skyline_client/monitor_worker.py"
            subprocess.call(["python", script_dir, monitor_conf, "%s" % monitor_idx])
        else:
            command = "skymonitor_worker"
            subprocess.call([command, monitor_conf, "%s" % monitor_idx])
    finally:
        os.kill(ppid, signal.SIGABRT)


def summary_worker_func(monitor_conf, monitor_idx):
    ppid = os.getppid()
    try:
        if DEBUG:
            script_dir = "/home/liuweibo/skyline/skyline_client/summary_worker.py"
            subprocess.call(["python", script_dir, monitor_conf, "%s" % monitor_idx])
        else:
            command = "skysummary_worker"
            subprocess.call([command, monitor_conf, "%s" % monitor_idx])
    finally:
        os.kill(ppid, signal.SIGABRT)


def warning_worker_func(warning_conf, log_path, warning_idx):
    ppid = os.getppid()
    try:
        if DEBUG:
            script_dir = "/home/liuweibo/skyline/skyline_client/warning_worker.py"
            subprocess.call(["python", script_dir, warning_conf, log_path, "%s" % warning_idx])
        else:
            command = "skywarning_worker"
            subprocess.call([command, warning_conf, log_path, "%s" % warning_idx])
    finally:
        os.kill(ppid, signal.SIGABRT)


def filter_func(monitor_conf, warning_conf):
    ppid = os.getppid()
    try:
        monitors = configure.get_monitors(monitor_conf)
        warnings = configure.get_warnings(warning_conf)

        log_path = configure.get_log_path(monitors)

        mw_list = []
        ww_list = []
        for i in range(len(monitors)):
            mw_list.extend([Process(target=monitor_worker_func, args=(monitor_conf, i)) for x in range(PROCESS_NUM)])
            mw_list.append(Process(target=summary_worker_func, args=(monitor_conf, i)))
        for i in range(len(warnings)):
            ww_list.append(Process(target=warning_worker_func, args=(warning_conf, log_path, i)))

        jobs = mw_list + ww_list

        for job in jobs:
            job.start()
        for job in jobs:
            job.join()

    finally:
        os.kill(ppid, signal.SIGABRT)


def gather_func(monitor_conf):
    ppid = os.getppid()
    try:
        # gather_dir = "skygather"
        # TODO: fix when release
        # subprocess.call([gather_dir, monitor_conf])
        subprocess.call(["python", "/home/liuweibo/skyline/skyline_client/gather.py", monitor_conf])
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
