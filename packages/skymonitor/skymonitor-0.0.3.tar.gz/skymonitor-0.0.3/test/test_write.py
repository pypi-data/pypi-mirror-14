#!/usr/bin/env python

from public import pubsub
import sys

#ps = pubsub.PubSub('/home/liuweibo/skyline/a.log')
ps = pubsub.PubSub("127.0.0.1:8999", pubsub.TCP)
while True:
    line = sys.stdin.readline()
    print "pub_message: ", line
    ps.pub_message("abc123")
