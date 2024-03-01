from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_project.settings')

app = Celery('employee_project')
app.conf.update(
    CELERY_FLOWER_URL_PREFIX='',
    FLOWER_BASIC_AUTH=[('admin', 'password123')]
)
app.conf.enable_utc = False

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")