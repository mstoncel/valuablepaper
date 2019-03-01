from celery.schedules import crontab
from celery.task import periodic_task
from app.api.helpers import all_initial_stock


@periodic_task(run_every=(crontab(hour=15, minute=8)))
def execute_function():
    all_initial_stock()
