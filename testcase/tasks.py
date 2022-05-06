from __future__ import absolute_import
from testcase.celery import app
import time


@app.task
def sleep_10_min():
    print('beginning to sleep 10 min')
    time.sleep(10*60)
    print('finished sleeping 10 min')
    return 0

@app.task
def sleep_5_sec():
    print('beginning to sleep 5 sec')
    time.sleep(5)
    print('finished sleeping 5 sec')
    return 0
