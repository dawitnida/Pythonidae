""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 20.10.2014"
__version__ = "Version: "

from datetime import datetime

from django_cron import CronJobBase, Schedule
from django.shortcuts import get_object_or_404
from django.utils import timezone

from yaas.models import Auction, AuctionStatus, AuctionBidder
from yaas.views import emailer, getBiddersEmail


class ResolveAuction(CronJobBase):
    RUN_EVERY_MINS = 1  # Every 60 seconds
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yaas.cron_resolvebid'

    def do(self):
        auctions = Auction.objects.filter(status_id=1)
        if auctions:
            for auc in auctions:
                now = timezone.now()
                if auc.end_time <= now:
                    any_bidder = AuctionBidder.objects.filter(auc=auc).count()
                    email_list = []
                    if any_bidder > 0:
                        auc.status_id = 4
                        email_list = getBiddersEmail(auc)
                        print "Auction %s is Adjudicated!" % auc.title
                    else:
                        auc.status_id = 3
                        print "Auction %s is Due!" % auc.title

                    auc.save(update_fields=['status_id'])

                    email_list.append(auc.product.seller.email)
                    emailer(str(email_list), "resolve", auc.title)
        else:
            print "Nothing to resolve!"


class CronAuctionBan(CronJobBase):
    RUN_EVERY_MINS = 1  # Every 1 minutes
    RETRY_AFTER_FAILURE_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'yaas.cronban'

    def do(self):
        auc = get_object_or_404(AuctionStatus, id=4, )
        auc.name = str(datetime.now())
        auc.save()
        print "I am running!"




