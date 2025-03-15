from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Configure the timezone
app.conf.enable_utc = False
app.conf.update(
                CELERY_WORKER_POOL='solo',
                timezone='Asia/Kathmandu'
                )

# Load configuration from Django settings
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-task-reminder-emails-daily': {
        'task': 'tasks.tasks.send_task_reminder_emails', 
        'schedule': crontab(minute=0, hour=0),
    },
    # 'send-test-email-every-minute': {
    #     'task': 'tasks.tasks.send_test_email',
    #     'schedule': crontab(minute=0, hour=0), 
    # },
}

# Autodiscover tasks in your apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
