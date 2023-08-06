#!/usr/bin/env python
#! coding: utf-8

import sys
import os
import hashlib
sys.path.append("..")
from skyconf import ZMQ_BIND_TO, ZMQ_CONNECT_TO
import zmq.green as zmq


MULTIPART = False
DEFAULT_PATH = "/tmp/zero_message_queue"
INPROC = "inproc://"
IPC = "ipc://"
TCP = "tcp://"


class Pub(object):
    def __init__(self, ctx, bind_to=ZMQ_BIND_TO, multipart=MULTIPART):
        self._ctx = ctx
        self._socket = self._ctx.socket(zmq.PUB)
        self._bind_to = bind_to
        self._socket.bind(self._bind_to)
        self._multipart = multipart

    def pub_message(self, message):
        if self._multipart:
            self._socket.send_multipart(message)
        else:
            self._socket.send(message)

    def get_socket(self):
        return self._bind_to


class Sub(object):
    def __init__(self, ctx, connect_to=ZMQ_CONNECT_TO, multipart=MULTIPART):
        self._ctx = ctx
        self._socket = self._ctx.socket(zmq.SUB)
        self._connect_to = connect_to
        self._socket.connect(self._connect_to)
        self._channel = ""
        self._socket.setsockopt(zmq.SUBSCRIBE, "")
        self._multipart = multipart

    def sub_message(self):
        if self._multipart:
            return self._socket.recv_multipart()
        else:
            return self._socket.recv()

    def set_channel(self, channel):
        self._socket.setsockopt(zmq.UNSUBSCRIBE, self._channel)
        self._socket.setsockopt(zmq.SUBSCRIBE, channel)
        self._channel = channel


class PubSub(object):
    '''
    1 to n publish-subscribe model implementation
    Notice: !!! No multi-threading supported !!!
    INPROC: pub and sub are in the same process and threading, eg: gevent
    IPC: inter-process-communication at same host
    TCP: over tcp/ip network communication
    '''
    def __init__(self, path=DEFAULT_PATH, proto_type=IPC, multipart=MULTIPART):
        self._ctx = zmq.Context()
        self.proto_type = proto_type
        if self.proto_type == IPC and not os.path.exists(path):
            raise Exception("Path: [%s] not exist!!" % path)
        self._path = path
        self._pub = None
        self._sub = []
        self._channel = ""
        self._multipart = multipart

    def _get_new_local_addr(self):
        if self.proto_type == IPC and not os.path.exists(self._path):
            raise Exception("Path: [%s] not exist!!" % self._path)
        addr = self.proto_type + self._path
        if self.proto_type != TCP:
            addr += ".zmq"
            hash_addr = hashlib.md5(addr).hexdigest()
            addr = self.proto_type + "/tmp/" + hash_addr + ".zmq"
        return addr

    def _get_pub(self):
        if self._pub is None:
            self._pub = Pub(self._ctx, self._get_new_local_addr(), self._multipart)
        return self._pub

    def create_sub(self):
        new_sub = Sub(self._ctx, self._get_new_local_addr(), self._multipart)
        self._sub.append(new_sub)
        return len(self._sub) - 1

    def pub_message(self, message):
        try:
            pub = self._get_pub()
        except:
            raise Exception("Already bind: [%s]" % self._get_new_local_addr())
        return pub.pub_message(message)

    def sub_message(self, sub=None):
        if sub is None:
            sub_idx = self.create_sub()
            self._sub[sub_idx].set_channel(self._channel)
            return self._sub[sub_idx].sub_message()
        return self._sub[sub].sub_message()

    def set_channel(self, channel=""):
        self._channel = channel
        for sub in self._sub:
            sub.set_channel(self._channel)
