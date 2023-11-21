import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'week_sender_8am': {
        'task': 'news.tasks.week_mail_to_subscribers',
        'schedule': crontab(minute='54', hour='21'),
        'args': None,
    },
}
