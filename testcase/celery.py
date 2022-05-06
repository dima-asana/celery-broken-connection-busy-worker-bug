from __future__ import absolute_import
from celery import Celery

app = Celery('testcase',
             broker='amqp://test:test@localhost/test_vhost',
             backend='rpc://',
             include=['testcase.tasks'])
