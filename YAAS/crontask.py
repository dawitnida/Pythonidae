""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 20.10.2014"
__version__ = "Version: "


from django_cron import CronJobBase, Schedule, CronJobManager
from django.shortcuts import get_object_or_404
from yaas.models import *
from datetime import datetime, date

# Check if the inserted date in valid
def validateDateTime(input_time):
    t_format = '%Y-%m-%d %H:%M:%S'
    end_time = datetime.strptime(input_time, t_format)
    now_str = datetime.now().strftime(t_format)
    now_dt = datetime.strptime(str(now_str), t_format)

    time_delta = end_time - now_dt
    sec = time_delta.total_seconds()

    if sec <= 0:
        return True
    else:
        return None

class ResolveAuction(CronJobBase):
    RUN_EVERY_MINS = 2      # Every 2 minutes
    RETRY_AFTER_FAILURE_MINS = 2

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS, retry_after_failure_mins= RETRY_AFTER_FAILURE_MINS)
    code = 'yaas.cron_endbid'


    def do(self):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a = get_object_or_404(Auction, status_id = 3,)
        if validateDateTime((a.end_time)):
            a.status_id = 1
            a.save()
            a.save(update_fields=['status_id'])
            print "I ended an auction %s!" %a.title

from threading import Timer
class CronAuctionBan(CronJobBase):
    RUN_EVERY_MINS = 1      # Every 2 minutes
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins = RUN_EVERY_MINS, retry_after_failure_mins= RETRY_AFTER_FAILURE_MINS)
    code = 'yaas.cronban'

    def do(self):
        auc = get_object_or_404(AuctionStatus, id = 4,)
        auc.name = str(datetime.now())
        auc.save()
        print "I am running!"




