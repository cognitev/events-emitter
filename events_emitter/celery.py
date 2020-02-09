from __future__ import unicode_literals, absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_emitter.settings')

app = Celery('events_emitter')

app.config_from_object(settings, namespace='CELERY')

app.conf.task_routes = {
    'events_emitter.tasks*': {'queue': settings.EVENTS_EMITTER_QUEUE},
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
