#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask_apscheduler import APScheduler
from fetcher.fetcher import main as fetcher
from fetcher.importor import main as importor


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:process',
            'trigger': 'interval',
            'seconds': 60 * 60 * 24
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True
    SCHEDULER_TIMEZONE = 'UTC'


def process():
    fetcher()
    importor()


app = Flask(__name__)
app.config.from_object(Config())


@app.route("/")
def hello():
    return "running..."


if __name__ == "__main__":
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')
