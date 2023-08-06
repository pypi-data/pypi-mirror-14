#!/usr/bin/env python
#! coding: utf-8

import os
import re
import simplejson
import time
import pyinotify
from jsonschema import validate
from formular import lexer


class MyEventHandler(pyinotify.ProcessEvent):
    def __init__(self, fw):
        super(MyEventHandler, self).__init__()
        self._file_watcher = fw
        self._file = fw._file
        self._file_dir = fw._file_dir
        self._file_name = fw._file_name
        self._file_path = fw._file_path

    def process_IN_MODIFY(self, event):
        if event.name == self._file_name:
            for line in self._file.readlines():
                self._file_watcher.pub_message(line)

    def process_IN_CREATE(self, event):
        if event.name == self._file_name:
            self._file = open(self._file_path)
            self._file_watcher._wm.add_watch(self._file_path,
                                             pyinotify.ALL_EVENTS,
                                             rec=True)


class FileWatcher(object):
    def __init__(self, conf, pub):
        self._file_path = conf["log_file_path"]
        self._file_dir = os.path.dirname(self._file_path)
        self._file_name = os.path.basename(self._file_path)
        self._name_prefix = conf["log_name_prefix"]
        self._pub = pub
        #self._msg_head = hashlib.md5(self._file_path).hexdigest()
        self._msg_head = ""

    def _set_loop_opt(self):
        max_try = 5
        try_cnt = 0
        while try_cnt < max_try:
            if os.path.exists(self._file_path):
                break
            else:
                print "[%s] not exist, retry:[%d] ..." % (self._file_path,
                                                          try_cnt)
                try_cnt += 1
                time.sleep(1)
        if max_try == try_cnt:
            raise Exception("[%s] not exist" % self._file_path)

        self._file = open(self._file_path, "r")
        assert(self._file)
        self._file.seek(0, 2)
        self._wm = pyinotify.WatchManager()
        self._eh = MyEventHandler(self)
        self._wm.add_watch(self._file_path, pyinotify.ALL_EVENTS, rec=True)
        self._wm.add_watch(self._file_dir, pyinotify.ALL_EVENTS, rec=True)
        self._notifier = pyinotify.Notifier(self._wm, self._eh)

    def start_loop(self):
        self._set_loop_opt()
        self._notifier.loop()

    def pub_message(self, message):
        self._pub.pub_message(self._msg_head + message)


_MonitorSchema = {
    "type": "object",
    "properties": {
        "log_name_prefix": {"type": "string"},
        "log_file_path": {"type": "string"},
        "filter_items": {"type": "array", "items": {"$ref": "#/definitions/monitor_item"}},
    },
    "required": ["log_name_prefix", "log_file_path", "filter_items"],
    "definitions": {
        "monitor_item": {
            "type": "object",
            "properties": {
                "item_name_prefix": {"type": "string"},
                "cycle": {"type": "integer"},
                "match_str": {"type": "string"},
                "threshold": {"type": "number"}
            },
            "required": ["item_name_prefix", "cycle", "match_str"],
        }
    },
}

_WarningSchema = {
    "type": "array",
    "items": {"$ref": "#/definitions/warning_item"},
    "definitions": {
        "warning_item": {
            "type": "object",
            "properties": {
                "warning_name": {"type": "string"},
                "formula": {"type": "string"},
                "waring_filter": {"type": "string"},
                "alert_name": {"type": "string"},
            },
            "required": ["warning_name", "formula", "warning_filter", "alert_name"]
        }
    }
}


def get_monitors(conf_path):
    verify_monitor_conf(conf_path)
    monitors = []
    with open(conf_path) as f:
        monitor_obj = simplejson.load(f)
        for monitor in monitor_obj["filter_items"]:
            m = {}
            m["log_name_prefix"] = monitor_obj["log_name_prefix"]
            m["log_file_path"] = monitor_obj["log_file_path"]
            m["item_name_prefix"] = monitor["item_name_prefix"]
            m["cycle"] = monitor["cycle"]
            m["match_str"] = monitor["match_str"]
            m["threshold"] = monitor.get("threshold", None)
            m["prefix"] = monitor_obj["log_name_prefix"] + "_" + monitor["item_name_prefix"]
            monitors.append(m)
    return monitors


def get_warnings(conf_path):
    verify_warning_conf(conf_path)
    warnings = []
    with open(conf_path) as f:
        warning_obj = simplejson.load(f)
        for warning in warning_obj:
            eval_str = warning["formula"]
            tokens = get_name_tokens(eval_str)
            n, d = get_filter_numerator_and_denominator(warning["warning_filter"])
            warning["numerator"] = n
            warning["denominator"] = d
            warning["tokens"] = ",".join(tokens)
            warnings.append(warning)
    return warnings


def verify_monitor_conf(conf_path):
    with open(conf_path) as f:
        variable_list = []
        items = []
        monitor_obj = simplejson.load(f)
        validate(monitor_obj, _MonitorSchema)
        log_name_prefix = monitor_obj["log_name_prefix"]
        for item in monitor_obj["filter_items"]:
            item_name_prefix = item["item_name_prefix"]
            if item_name_prefix in items:
                raise Exception("key[%s] item_name_prefix repeated!" %
                                item_name_prefix)
            else:
                items.append(item_name_prefix)
            name = log_name_prefix + "_" + item_name_prefix
            variable_list.append(name)
        print "monitor verify done"
        return variable_list


def get_name_tokens(eval_str):
    variable_list = []
    lexer.input(eval_str)
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type == "NAME":
            variable_list.append(tok.value)
    return variable_list


def get_filter_numerator_and_denominator(filter_str):
    pattern = re.compile(r"^\s*(\d*)\s*/\s*(\d*)\s*$")
    g = pattern.match(filter_str)
    if not g:
        raise Exception("filter format error: [%s]" % filter_str)
    numerator = int(g.group(1))
    denominator = int(g.group(2))
    if numerator > denominator:
        raise Exception("formula numerator[%d] is greater than denominator[%d]" %
                        numerator, denominator)
    return numerator, denominator


def verify_warning_conf(conf_path):
    variable_list = []
    with open(conf_path) as f:
        warning_obj = simplejson.load(f)
        validate(warning_obj, _WarningSchema)
        for warning in warning_obj:
            eval_str = warning["formula"]
            new_list = get_name_tokens(eval_str)
            if len(new_list) > 1:
                raise Exception("too many variable in formula:[%s]" %
                                ";".join(new_list))
            variable_list += new_list

            f = warning["warning_filter"]
            get_filter_numerator_and_denominator(f)

    return variable_list
