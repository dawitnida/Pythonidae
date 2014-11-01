""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 20.10.2014"
__version__ = "Version: "

from celery.schedules import crontab
from celery.task import periodic_task
import django

from yaas.management.commands.resolve import Command
from yaas.crontask import ResolveAuction

django.setup()

# Amazingly done after lots of research.
# This does the real resolving process with just calling the main
# class that does the hard work from ResolveAuction class
# This is pretty neat when it works with celery...
# seems less work of 2 continues days to configure cron tab on django + WINDOWS machine Snap! I miss Linux-
# Run crontab job...will execute command every minute.
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def run_crontask():
    auto = Command()
    auto.handle_noargs()


# Same work without django_cron for clarity and no custom management command
def run_crontask_direct():
    res = ResolveAuction()
    res.do()
