#!/usr/bin/env python
# coding: utf-8


import sys
from public import configure
from worker import WarningWorker


def warning_worker_main():
    warning_conf = sys.argv[1]
    log_path = sys.argv[2]
    warning_idx = int(sys.argv[3])

    warnings = configure.get_warnings(warning_conf)
    my_warning = warnings[warning_idx]
    my_warning_worker = WarningWorker(my_warning, log_path)

    my_warning_worker.work()


if __name__ == "__main__":
    warning_worker_main()
