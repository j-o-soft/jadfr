from __future__ import absolute_import
import os


import ipdb; ipdb.set_trace()
from celery import Celery


from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jadfr.settings')

app = Celery('jadfr')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)