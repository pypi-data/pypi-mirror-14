#!/usr/bin/env python

from public import pubsub

#ps = pubsub.PubSub('/home/liuweibo/skyline/a.log')
ps = pubsub.PubSub('127.0.0.1:8999', pubsub.TCP)
sb = ps.create_sub()
ps.set_channel("abc")
while True:
    print "sub_message: ", ps.sub_message(sb)
