"""Celery configuration."""
import os
import logging

from celery import Celery

from decouple import config

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_board.settings')


app = Celery('job_board', broker=config('REDIS_URL'))


# Load the celery settings from the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['talentpool.application.services'])

LOG = logging.getLogger(__name__)

app.conf.beat_schedule = {
    'publish_scheduled_job_adverts': {
        'task': 'talentpool.application.services.publish_scheduled_job_adverts',
        'schedule': 60.0,
    },
}
