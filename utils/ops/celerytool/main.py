# coding:utf-8

import psutil
from celery import  Celery
from utils.ops.celerytool import config
celery_app = Celery("my_tasks")
celery_app.config_from_object(config)
celery_app.autodiscover_tasks(["utils.ops.celerytool.ansible_task"])

psutil.disk_io_counters()

