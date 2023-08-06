#!/usr/bin/env python
# coding: utf-8


import sys
from public import configure
from worker import SummaryWorker


def summary_worker_main():
    monitor_conf = sys.argv[1]
    monitor_idx = int(sys.argv[2])

    monitors = configure.get_monitors(monitor_conf)
    monitor = monitors[monitor_idx]
    summary_worker = SummaryWorker(monitor)

    summary_worker.work()


if __name__ == "__main__":
    summary_worker_main()
