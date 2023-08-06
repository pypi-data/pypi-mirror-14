#!/usr/bin/env python
# coding: utf-8


import sys
from public.configure import verify_monitor_conf, verify_warning_conf


def verify_main():
    if len(sys.argv) < 3:
        print "usage: skyverify monitor_conf warning_conf"
        exit(1)
    monitor_conf = sys.argv[1]
    warning_conf = sys.argv[2]

    m_vars = verify_monitor_conf(monitor_conf)
    w_vars = verify_warning_conf(warning_conf)

    all_set = []
    for var in m_vars:
        all_set.extend([var+"_cps", var+"_cnt", var+"_avg"])

    for var in w_vars:
        if var not in all_set:
            print ("var:[%s] not in" % var), all_set

    return 0


if __name__ == "__main__":
    verify_main()
