# -*- coding:utf-8 -*-

from __future__ import absolute_import

try:
    from django.conf import settings
except ImportError:
    import config as settings

from celery import Celery

app = Celery('anti',
             broker=settings.ANTI_REDIS_CONF_URI,
             backend=settings.ANTI_REDIS_CONF_URI,
             include=['anti.anti'])

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
