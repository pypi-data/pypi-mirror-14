#!/usr/bin/env python
# coding: utf-8

import os
import sys
sys.path.append("/ect/skyline/")

DEBUG = False

try:
    # from test_conf import * # noqa
    from online_conf import * # noqa
except:
    raise Exception("Please configure /etc/skyline/ directory!")
# from dev_conf import * # noqa


def get_email_list(alert_name):
    global WARNIG_ALERT
    for w in WARNING_ALERT:
        if w.get("name", None) == alert_name:
            return w.get("emails", [])


def get_phone_list(alert_name):
    global WARNIG_ALERT
    for w in WARNING_ALERT:
        if w.get("name", None) == alert_name:
            return w.get("phones", [])


def get_host_name():
    hostname = os.popen("hostname").read().strip()
    return hostname
