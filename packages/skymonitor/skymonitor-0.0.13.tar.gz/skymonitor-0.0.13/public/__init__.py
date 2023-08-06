#!/usr/bin/env python
# coding: utf-8

import os
import signal
import pubsub # noqa
import configure # noqa
from functools import wraps


def exit_whole_process(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ppid = os.getppid()
        try:
            func(*args, **kwargs)
        finally:
            os.kill(ppid, signal.SIGABRT)
    return wrapper
