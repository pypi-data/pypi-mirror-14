#!/usr/bin/env python
# coding: utf-8

import os
import sys
import hashlib
sys.path.append("..")
import zmq


PROC_TYPE_INPROC = "inproc://"  #local in-process (inter-thread) communication transport, see zmq_inproc(7)
PROC_TYPE_IPC = "ipc://"        #local inter-process communication transport, see zmq_ipc(7)
PROC_TYPE_TCP = "tcp://"        #unicast transport using TCP, see zmq_tcp(7)
PROC_TYPE_PGM = "pgm://"        #reliable multicast transport using PGM, see zmq_pgm(7)

PUB = zmq.PUB
SUB = zmq.SUB
PUSH = zmq.PUSH
PULL = zmq.PULL


class MQ(object):

    def __init__(self, addr, mq_model_type, bind_flag, connect_flag, ctx):
        self.addr = addr

        if ctx is None:
            self.ctx = zmq.Context()
        else:
            self.ctx = ctx
        self.socket = self.ctx.socket(mq_model_type)
        if bind_flag:
            self.socket.bind(self.addr)
        if connect_flag:
            self.socket.connect(self.addr)


class MQSender(MQ):

    def __init__(self, path, proto_type=PROC_TYPE_IPC, mq_model_type=PUB, bind_flag=True, connect_flag=False, multipart=False, ctx=None):
        self.path = path
        self.proto_type = proto_type
        self.multipart = multipart
        self.mq_model_type = mq_model_type
        self.addr = self.get_addr_from_path()
        super(MQSender, self).__init__(self.addr, mq_model_type,
                                       bind_flag, connect_flag,
                                       ctx)

    def send_message(self, message):
        if self.multipart:
            self.socket.send_multipart(message)
        else:
            self.socket.send(message)

    def get_addr_from_path(self):
        if self.proto_type == PROC_TYPE_IPC and not os.path.exists(os.path.dirname(self.path)):
            raise Exception("Path:[%s] not exists!!" % self.path)
        addr = self.proto_type + self.path
        if self.proto_type != PROC_TYPE_TCP:
            addr_md5 = hashlib.md5(addr).hexdigest()
            addr = self.proto_type + "/tmp/" + addr_md5 + ".zmq"
        return addr


class MQReceiver(MQ):

    def __init__(self, path, proto_type=PROC_TYPE_IPC, mq_model_type=SUB, bind_flag=False, connect_flag=True, multipart=False, ctx=None):
        self.path = path
        self.proto_type = proto_type
        self.multipart = multipart
        self.mq_model_type = mq_model_type
        self.addr = self.get_addr_from_path()
        super(MQReceiver, self).__init__(self.addr, mq_model_type,
                                         bind_flag, connect_flag,
                                         ctx)

        if self.mq_model_type == SUB:
            self.socket.setsockopt(zmq.SUBSCRIBE, "")

    def receive_message(self):
        if self.multipart:
            return self.socket.recv_multipart()
        else:
            return self.socket.recv()

    def get_addr_from_path(self):
        if self.proto_type == PROC_TYPE_IPC and not os.path.exists(os.path.dirname(self.path)):
            raise Exception("Path:[%s] not exists!!" % self.path)
        addr = self.proto_type + self.path
        if self.proto_type != PROC_TYPE_TCP:
            addr_md5 = hashlib.md5(addr).hexdigest()
            addr = self.proto_type + "/tmp/" + addr_md5 + ".zmq"
        return addr
