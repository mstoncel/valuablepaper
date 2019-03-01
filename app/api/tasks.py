from celery.schedules import crontab
from celery.task import periodic_task
from app.api.helpers import all_initial_stock


@periodic_task(
    run_every=(crontab(minute='*/30', day_of_week='mon,tue,wed,thu,fri')))
def execute_task():
    all_initial_stock()
