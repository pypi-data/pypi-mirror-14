#!/usr/bin/env python
# coding: utf-8


import sys
from public import configure
from worker import MonitorWorker


def monitor_worker_main():
    monitor_conf = sys.argv[1]
    monitor_idx = int(sys.argv[2])

    monitors = configure.get_monitors(monitor_conf)
    my_monitor = monitors[monitor_idx]
    my_monitor_worker = MonitorWorker(my_monitor)

    my_monitor_worker.work()


if __name__ == "__main__":
    monitor_worker_main()
