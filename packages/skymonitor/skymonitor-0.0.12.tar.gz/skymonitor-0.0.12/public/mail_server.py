#!/usr/bin/env python
#coding:utf8
import requests


class SendCloud(object):
    '''
    封装了第三方的send cloud服务，用web api方式发送邮件
    官方提供的例子见http://sendcloud.sohu.com/sendcloud/api-doc/web-api-python-examples
    '''

    def __init__(self, url, api_user, api_key, default_from_name, default_from_mail):
        self.url = url
        self.api_user = api_user
        self.api_key = api_key
        self.default_from_name = default_from_name
        self.default_from_mail = default_from_mail

    def send_mail(self, to_mail, title, body, from_mail=None, from_name=None, files={}):
        from_mail = from_mail or self.default_from_mail
        from_name = from_name or self.default_from_name
        params = {
            "api_user": self.api_user,
            "api_key": self.api_key,
            "to": to_mail,
            "from": from_mail,
            "fromname": from_name,
            "subject": title,
            "html": body
        }

        r = requests.post(self.url, files=files, data=params)
        return r.text
