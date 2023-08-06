#!/usr/bin/env python
# coding: utf-8

import re
import time
from collections import deque, namedtuple
from public import alert, communicate
from skyconf import get_email_list, get_phone_list, get_host_name, ALERT_URL


class MonitorWorker(object):

    def __init__(self, conf_dict):
        super(MonitorWorker, self).__init__()
        self._conf = conf_dict
        self._path = conf_dict["log_file_path"]
        self._cycle = conf_dict["cycle"]
        self._threshold = conf_dict.get("threshold", None)
        self._prefix = conf_dict["prefix"]
        self.match_str = conf_dict["match_str"]
        self.pattern = re.compile(self.match_str)
        self.sub = communicate.MQReceiver(self._path, mq_model_type=communicate.PULL)
        self.pub = communicate.MQSender(self._path+".filter", mq_model_type=communicate.PUSH, ctx=self.sub.ctx, bind_flag=False, connect_flag=True)

        self._total = 0
        self._cnt = 0
        self._avg = 0
        self._cps = 0
        self._time = int(time.time())
        self._cycle_id = int(time.time() / self._cycle)

    def work(self):
        while True:
            log_message = self.sub.receive_message()
            result = self.pattern.search(log_message)
            if not result:
                # cannot match
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
            self.pub.send_message("%s" % number)


class SummaryWorker(object):

    def __init__(self, conf_dict):
        super(SummaryWorker, self).__init__()
        self._conf = conf_dict
        self._path = conf_dict["log_file_path"]
        self._cycle = conf_dict["cycle"]
        self._token = conf_dict["prefix"]
        self.match_str = conf_dict["match_str"]
        self.sub = communicate.MQReceiver(self._path+".filter", mq_model_type=communicate.PULL, bind_flag=True, connect_flag=False)
        self.pub = communicate.MQSender(self._path+"."+self._token, multipart=True)

        self._total = 0
        self._cnt = 0
        self._avg = 0
        self._cps = 0
        self._time = int(time.time())
        self._cycle_id = int(time.time() / self._cycle)

    def work(self):
        while True:
            number = self.sub.receive_message()
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
        self.pub.send_message(message)
        self._cps = 0
        self._time = new_time


class WarningWorker(object):
    CycleRecord = namedtuple("CycleRecord", ["cid", "warning_flag", "cnt", "avg", "cps"])

    def __init__(self, conf_dict, log_path, alert_url=ALERT_URL):
        super(WarningWorker, self).__init__()
        self._path = log_path
        self._warning_name = conf_dict["warning_name"]
        self._formula = conf_dict["formula"]
        self._warning_filter = conf_dict["warning_filter"]
        self._numerator = conf_dict["numerator"]
        self._denominator = conf_dict["denominator"]
        self._alert_name = conf_dict["alert_name"]
        # only one token at one time
        # TODO: hard coding
        # FIXME: hard coding
        self._token = conf_dict["tokens"][:-4]
        self.warning_queue = deque(maxlen=self._denominator)
        self.last_cid = 0
        self.alert_url = alert_url

        self.sub = communicate.MQReceiver(self._path+"."+self._token, multipart=True)

    def work(self):
        while True:
            ts, cid, cnt, avg, cps = self.sub.receive_message()
            # TODO
            print "receive msg:", ts, cid, cnt, avg, cps
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

        try:
            alert.send_alert(**params)
        except Exception as e:
            print "error when sending alert:", e


def test_worker(path):
    print "test_worker start"
    sub = communicate.MQReceiver(path+".filter", multipart=True)
    while True:
        msg = sub.receive_message()
        print "test_worker recerive a msg:", msg
