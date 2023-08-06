#!/usr/bin/env python
#! coding: utf-8

import gevent
from gevent import queue
import configure

interval = 0.1 # 0.1 second


class FileWatcher():

    def __init__(self, monitors, monitor_filter_queues):
        self._monitors = monitors
        self._monitor_filter_queues = monitor_filter_queues

    def start_watch_loop(self):
        while True:
            print "passive loop forever"

    def on_event_file_modify(self, event):
        dispatch_file_mod(event.message, self._monitor_filter_queues)


def dispatch_file_mod(log_message, monitor_filter_queues):
    for i in monitor_filter_queues:
        i.put(log_message)


class WarningFilter():

    def __init__(self, warning, warning_filter_queues):
        self._name = warning.name
        self._formula = warning.formula
        self._trigger_cycle = warning.trigger_cycle
        self._continuous_cycle = warning.continuous_cycle
        self._alert = warning.alert

    def proc_match_result(self, result):
        pass

    def send_alert(self):
        pass


class MonitorFilter():

    def __init__(self, monitor, monitor_filter_queue, warning_filters):
        self._monitor = monitor
        self._monitor_filter_queue = monitor_filter_queue
        self._warning_filters = warning_filters

    def work(self):
        while True:
            log_message = self._monitor_filter_queue.get()
            match_result = self.filter_message(log_message)
            for warning_filter in self._warning_filters:
                warning_filter.proc_match_result(match_result)


def set_monitor_and_warning():
    monitors = configure.get_monitors()
    warnings = configure.get_warnings()
    monitor_cnt = len(monitors)

    monitor_filter_queues = [queue.Queue() for i in xrange(monitor_cnt)]
    workers = [MonitorFilter(monitors[i], monitor_filter_queues[i], warnings) for i in xrange(monitor_cnt)]

    file_watcher = FileWatcher(monitors, monitor_filter_queues)
    jobs = [
        gevent.spawn(file_watcher.start_watch_loop),
    ] + [
        gevent.spwan(worker.work) for worker in workers
    ]
    return jobs
    #gevent.joinall(jobs)


if __name__ == "__main__":
    jobs = set_monitor_and_warning()
    gevent.joinall(jobs)
