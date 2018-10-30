# coding:utf-8


BROKER_URL = 'redis://127.0.0.1:7000/0'               # 指定 Broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:7001/0'  # 指定 Backend
CELERY_TIMEZONE='Asia/Shanghai'                     # 指定时区，默认是 UTC
CELERYD_MAX_TASKS_PER_CHILD = 40     # 每个worker执行了多少任务就会死掉,防止内存泄露


