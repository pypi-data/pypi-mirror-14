#!/usr/bin/env python
# coding: utf-8

from flask import request
from skyline.views.lib.render import ok, error
from skyline.views.api import api_bp
from public import alert


def get_param(key):
    value = request.args.get(key, None)
    if value is None:
        raise Exception(("[%s] is None" % key))
    return value


@api_bp.route("/alert/send_alert.json", methods=["GET", "POST"])
def send_alert():
    """
    测试命令:
        curl -G --data-urlencode 'machine=local_machine' --data-urlencode 'title=warning' --data-urlencode 'contents=绑定成功！您已获得20元优惠券，打开下厨房APP，到市集挑选你喜爱的食物和餐 具吧！http://t.cn/R4Njydl' --data-urlencode 'phone_numbers=18600314095' --data-urlencode 'email_addrs=liuweibo@xiachufang.com' 'http://127.0.0.1:9999/api/alert/send_alert.json'
    """
    try:
        machine = get_param("machine")
        title = get_param("title")
        contents = get_param("contents").encode("utf-8")
        phone_numbers = get_param("phone_numbers").split(",")
        email_addrs = get_param("email_addrs")
    except Exception as e:
        return error("required parameter: %s" % e, 400)

    email_ret, sms_ret = alert.send_alert(machine, title, contents, phone_numbers, email_addrs)
    return ok({
        "result": "ok",
        "email_ret": email_ret,
        "sms_ret": sms_ret
    })
