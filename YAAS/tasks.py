""" Development of Web Applications and Web Services

"""
from __future__ import absolute_import

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 24.10.2014"
__version__ = "Version: "

from yaas.yaascelery import app
from yaas.models import Auction, AuctionBidder
from django.utils import timezone
from yaas.views import emailer, getBiddersEmail


@app.task
def sthng():
    print 'I am running celery'


@app.task
def resolve_auction():
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

