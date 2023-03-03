from celery.schedules import crontab  # type: ignore

from .app import app

app.conf.beat_schedule = {}
