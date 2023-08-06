#!/usr/bin/env python
#! coding: utf-8

import sys
from collections import Counter
from public import configure


def start():
    pass


def stop():
    pass


def restart():
    pass


def verify(monitor_conf, warning_conf):
    monitor_var = configure.verify_monitor_conf(monitor_conf)
    warning_var = configure.verify_warning_conf(warning_conf)
    var_legal = []
    format_str = "error: %s is not unique, repeat for %d times"
    duplicated_items = [format_str % (k, v) for k, v in
                        dict(Counter(monitor_var)).items() if v > 1]
    if duplicated_items:
        raise Exception(";".join(duplicated_items))
    for m in monitor_var:
        var_legal.append(m + "_cnt")
        var_legal.append(m + "_avg")
        var_legal.append(m + "_cps")
    for w in warning_var:
        if w not in var_legal:
            raise Exception("[%s] [%s] configure verify failed, [%s] failed" %
                            (monitor_conf, warning_conf, w))
    print "verify %s %s success" % (monitor_conf, warning_conf)


def how_to_use():
    print "usage: skyline_ctrl.py [start|restart|stop] or skyline_ctr.py verify monitor.conf warning.conf"
    exit(-1)

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 5:
        how_to_use()
    option = sys.argv[1]
    if option == "start":
        verify(sys.argv[2], sys.argv[3])
        start()
    elif option == "stop":
        stop()
    elif option == "restart":
        verify(sys.argv[2], sys.argv[3])
        restart()
    elif option == "verify":
        verify(sys.argv[2], sys.argv[3])
    else:
        how_to_use()
