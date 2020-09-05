import os
from celery import Celery, platforms
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','analyze.settings')
# os.environ.setdefault('SCRAPY_SETTINGS_MODULE','analyze.phone.spider.spider.settings')
app = Celery('analyze')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True


@app.task(bind=True)    #将函数封装成任务。
def debug_task(self):
    print('Request: {0!r}'.format(self.request))