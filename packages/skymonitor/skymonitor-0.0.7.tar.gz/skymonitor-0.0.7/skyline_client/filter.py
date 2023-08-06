#!/usr/bin/env python
# coding: utf-8

import gevent
from gevent import monkey
monkey.patch_all()
import re
import sys
import time
import subprocess
from collections import deque, namedtuple
from multiprocessing import Process
from public import pubsub, configure, alert
from skyconf import get_email_list, get_phone_list, get_host_name, ALERT_URL


prefix_pubsub_dict = {}


class MonitorWorker(object):

    def __init__(self, conf_dict, prefix_pubsub_dict):
        super(MonitorWorker, self).__init__()
        self._conf = conf_dict
        self._path = conf_dict["log_file_path"]
        self._cycle = conf_dict["cycle"]
        self._threshold = conf_dict.get("threshold", None)
        self._prefix = conf_dict["prefix"]
        self.match_str = conf_dict["match_str"]
        self.pattern = re.compile(self.match_str)
        self.sub = pubsub.PubSub(self._path,)
        print "mw path:", self._path
        self.sub_idx = self.sub.create_sub()
        self.pub = pubsub.PubSub(self._prefix, pubsub.INPROC, multipart=True)

        prefix_pubsub_dict[self._prefix] = self.pub

        self._total = 0
        self._cnt = 0
        self._avg = 0
        self._cps = 0
        self._time = int(time.time())
        self._cycle_id = int(time.time() / self._cycle)

    def work(self):
        print "MonitorWorker work start"
        while True:
            log_message = self.sub.sub_message(self.sub_idx)
            result = self.pattern.search(log_message)
            if not result:
                continue
            if result.groups():
                result = result.group(1)
            else:
                # no capture group, no '()' in regex string
                result = 0
            try:
                number = float(result)
            except:
                number = 0
            if self._threshold is not None and number < self._threshold:
                continue
            self.process_new_record(number)

    def process_new_record(self, rec):
        self._total += float(rec)
        self._cnt += 1
        self._avg = self._total / self._cnt
        self._cps += 1

        new_time = int(time.time())
        new_cycle_id = int(time.time() / self._cycle)
        if new_cycle_id > self._cycle_id:
            self.on_cycle_arrived(new_time, new_cycle_id)
        elif new_time > self._time:
            self.on_second_arrived(new_time, new_cycle_id)

    def on_cycle_arrived(self, new_time, new_cycle_id):
        self.on_second_arrived(new_time, new_cycle_id)
        self._total = 0
        self._cnt = 0
        self._avg = 0
        self._cycle_id = new_cycle_id

    def on_second_arrived(self, new_time, new_cycle_id):
        # FIXME: serial data into binary form, not use string instead
        message = [new_time, new_cycle_id, self._cnt, self._avg, self._cps]
        for i in xrange(len(message)):
            message[i] = "%s" % message[i]
        self.pub.pub_message(message)
        self._cps = 0
        self._time = new_time


class WarningWorker(object):
    CycleRecord = namedtuple("CycleRecord", ["cid", "warning_flag", "cnt", "avg", "cps"])

    def __init__(self, conf_dict, prefix_pubsub_dict, alert_url=ALERT_URL):
        super(WarningWorker, self).__init__()
        self._warning_name = conf_dict["warning_name"]
        self._formula = conf_dict["formula"]
        self._warning_filter = conf_dict["warning_filter"]
        self._numerator = conf_dict["numerator"]
        self._denominator = conf_dict["denominator"]
        self._alert_name = conf_dict["alert_name"]
        # only one token at one time
        self._token = conf_dict["tokens"][:-4]
        self.warning_queue = deque(maxlen=self._denominator)
        self.last_cid = 0
        self.alert_url = alert_url

        def get_sub(token, prefix_pubsub_dict):
            return prefix_pubsub_dict[token]
        self.sub = get_sub(self._token, prefix_pubsub_dict)
        self.sub_idx = self.sub.create_sub()

    def work(self):
        while True:
            ts, cid, cnt, avg, cps = self.sub.sub_message(self.sub_idx)
            ts = int(ts)
            cid = int(cid)
            cnt = float(cnt)
            avg = float(avg)
            cps = int(cps)
            var_dict = {
                "%s_cnt" % self._token: cnt,
                "%s_avg" % self._token: avg,
                "%s_cps" % self._token: cps,
            }

            if self.last_cid != cid:
                # if there is a new cid, update the warning queue
                wf = None
                if eval(self._formula, var_dict):
                    wf = True
                else:
                    wf = False
                cr = WarningWorker.CycleRecord(cid=cid, warning_flag=wf, cnt=cnt, avg=avg, cps=cps)
                print "cid:", cid, " warnig_flag:", wf, " cnt:", cnt, " avg:", avg, " cps:", cps
                self.warning_queue.append(cr)
                self.last_cid = cid

                satisfied_cnt = 0
                for wcr in self.warning_queue:
                    if wcr.warning_flag:
                        satisfied_cnt += 1
                if satisfied_cnt >= self._numerator:
                    self.send_warning()

    def send_warning(self):
        email_list = ";".join(get_email_list(self._alert_name))
        phone_list = (get_phone_list(self._alert_name))
        title = "warning"
        contents = "warning[%s] is triggered!" % self._warning_name
        hostname = get_host_name()

        params = {
            "machine": hostname,
            "title": title,
            "contents": contents,
            "phone_numbers": phone_list,
            "email_addrs": email_list
        }

        alert.send_alert(**params)


def test_worker():
    global prefix_pubsub_dict
    print prefix_pubsub_dict
    sub = prefix_pubsub_dict.values()[0]
    idx = sub.create_sub()
    print "test_worker start"
    while True:
        msg = sub.sub_message(idx)
        print "test_worker recerive a msg:", msg


def how_to_use():
    print "usage: filter.py monitor.conf warning.conf"
    exit(-1)


def filter_func(monitor_conf, warning_conf):
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


def gather_func(monitor_conf):
    gather_dir = "skygather"
    subprocess.call([gather_dir, monitor_conf])


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
