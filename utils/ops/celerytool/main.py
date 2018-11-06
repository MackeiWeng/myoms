# coding:utf-8

from celery import  Celery
from utils.ops.celerytool import celeryconfig
import logging.config

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            # 'datefmt': '%m-%d-%Y %H:%M:%S'
            'format': '%(asctime)s-%(name)s-%(levelname)s-%(filename)s-%(message)s'
        }
    },
    'handlers': {
        'celery': {
            # 'level': 'INFO',
            # 'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'mycelery.log',
            'when': 'midnight'
        },
    },
    'loggers': {
         'ansible_task': {
            'handlers': ['celery'],
            'level': 'INFO',
            'propagate': True,
         }
    }
}


celery_app = Celery("my_tasks")
celery_app.config_from_object(celeryconfig)
celery_app.autodiscover_tasks(["utils.ops.celerytool.ansible_task"])
logging.config.dictConfig(LOG_CONFIG)



