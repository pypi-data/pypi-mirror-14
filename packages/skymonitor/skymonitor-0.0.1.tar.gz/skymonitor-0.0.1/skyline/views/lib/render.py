#!/usr/bin/env python
# coding: utf-8
import simplejson
from flask import Response


def jsonify(data, status):
    return Response(simplejson.dumps(data),
        mimetype='application/json', status=status)


def ok(content='', status=200):
    msg = {
        'status': 'ok',
        'content': content,
    }

    resp = jsonify(msg, status)
    return resp


def error(error='', status=400):
    if isinstance(error, (tuple, list)):
        msg = {
            'status': 'error',
            'code': error[0],
            'msg': error[1],
        }
    else:
        msg = {
            'status': 'error',
            'msg': error,
        }

    resp = jsonify(msg, status)
    return resp
