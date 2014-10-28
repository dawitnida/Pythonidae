""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 20.10.2014"
__version__ = "Version: "

from django_cron import CronJobBase, Schedule
from django.utils import timezone

from yaas.models import Auction, AuctionBidder
from yaas.views import emailer, getBiddersEmail, getHighestBidder, email_winner


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
                    if any_bidder > 0:
                        auc.status_id = 4
                        auc.save(update_fields=['status_id'])
                        email_list = getBiddersEmail(auc)
                        winner = getHighestBidder(auc)[0]
                        win_price = getHighestBidder(auc)[1]
                        arg = (auc.title, winner, win_price)
                        email_list.append(auc.product.seller.email)
                        email_winner(str(email_list), arg)
                    else:
                        auc.status_id = 3
                        auc.save(update_fields=['status_id'])
                        email_list = auc.product.seller.email
                        emailer(str(email_list), "due", auc.title)
        else:
            print "Nothing to resolve!"




