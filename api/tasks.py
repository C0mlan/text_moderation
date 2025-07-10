from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import now
from datetime import timedelta
from .models import MyAPIKey


def reset_keylimit():
    current_time = now()
    keys = MyAPIKey.objects.all()

    for key in keys:
        if key.last_reset is None or (current_time - key.last_reset) >= timedelta(minutes=9):
            key.usage_count = 0
            key.last_reset = current_time
            key.save()
            print(f"[{current_time}] Usage reset triggered for {key.user.username}")

#starts the ApSchedular
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_keylimit, 'cron', minute ='*/10')
    scheduler.start()
     
    