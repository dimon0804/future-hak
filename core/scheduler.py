# myapp/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from .utils import parse_news
import time

def start(request):
    print("Scheduler started") 
    scheduler = BackgroundScheduler()
    scheduler.add_job(parse_news, 'interval', hours=12)
    scheduler.start()

    def job_listener(event):
        if event.exception:
            print(f"Task {event.job_id} failed")
        else:
            print(f"Task {event.job_id} succeeded")

    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

    try:
        # keep the main thread alive to allow the background scheduler to run
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
