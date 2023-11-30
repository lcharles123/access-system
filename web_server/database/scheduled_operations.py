from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from datetime import datetime, timedelta

from .models import Permissions, Entry_List
from . import db


''' This is a scheduled job to clean periodically
    The entries is guaranted to have at least 6 months before cleanup
''' 
def delete_entries_older_than(days=366/2 + 1):
    days_ago = datetime.utcnow() - timedelta(days=days)
    Entry_List.query.filter(Entry_List.date < days_ago).delete()
    db.session.commit()

def delete_scheduled_permission():
    now = datetime.utcnow()
    expired = Permissions.query.filter(Permissions.expires == True, 
                                       Permissions.expiration_date < now).all()
    for p in expired_permissions:
        db.session.delete(p)
    db.session.commit()

''' Remove entries older than x days
'''
def add_sched_entries():
    sched = BackgroundScheduler()
    sched.add_job(delete_entries_older_than, trigger='cron', hour=0, minute=0)
    sched.add_job(
    delete_scheduled_permission,
    trigger=IntervalTrigger(days=1),
    name='Check and revoke permissions every day',
    replace_existing=True)
    atexit.register(lambda: scheduler.shutdown())
    
    return sched
    
''' Remove permissions if expired
'''
def start_sched(scheduler):
    scheduler.start()

