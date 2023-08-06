#!/usr/bin/env python
# coding: utf-8
import logging
from flask import Flask
from flask.ext.mako import MakoTemplates, render_template
from werkzeug.contrib.fixers import ProxyFix
from raven.contrib.flask import Sentry
from skyconf import DEBUG
from public.logger import syslogger_handler


app = Flask(__name__)
app.config.from_object('skyline.settings')

mako = MakoTemplates(app)

app.wsgi_app = ProxyFix(app.wsgi_app)

if not DEBUG:
    sentry = Sentry(app)

app.logger.addHandler(syslogger_handler('skyline', loglevel=logging.WARN))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


def register_blueprint(app):
    from skyline.views import api
    app.register_blueprint(api.api_bp, url_prefix='/api')


register_blueprint(app)


import skyline.views.api.alert  # noqa


if __name__ == "__main__":
    app.run(debug=True)
