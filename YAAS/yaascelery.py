""" Development of Web Applications and Web Services

"""
from __future__ import absolute_import


__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 24.10.2014"
__version__ = "Version: "

from celery import Celery

app = Celery('yaas',
             include=['yaas.tasks'])

if __name__ == '__main__':
    app.start()