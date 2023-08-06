#!/usr/bin/env python
# coding: utf-8

import time
from skyconf.init_db import internal_mail_server, sms


def send_alert_by_sms(phone_numbers, title, contents, country_code="86"):
    result = 0
    for phone_number in phone_numbers:
        msg = (title.encode("utf-8") +
               "\n" +
               contents)
        ret = sms.send_plain_text(country_code, phone_number, msg)
        if ret != 0:
            result = ret
    return result


def send_alert_by_email(email_addrs, title, body):
    return internal_mail_server.send_mail(email_addrs, title=title, body=body)


def send_alert(machine, title, contents, phone_numbers, email_addrs):

    cur_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    title = u"!!! 警告 !!! #%s# #%s# %s" % (machine, cur_time, title)
    email_ret = send_alert_by_email(email_addrs,
                                    title,
                                    contents)

    sms_ret = send_alert_by_sms(phone_numbers,
                                title,
                                contents)
    return email_ret, sms_ret
