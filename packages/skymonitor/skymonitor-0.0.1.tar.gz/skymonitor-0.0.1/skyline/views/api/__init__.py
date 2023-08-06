#!/usr/bin/env python
# coding: utf-8

from flask import Blueprint


api_bp = Blueprint("api", __name__)


import skyline.views.api.alert # noqa
