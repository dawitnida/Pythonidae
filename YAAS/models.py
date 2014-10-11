from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode
from datetime import datetime


class ProductCategory(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return smart_unicode(self.name)


class Product(models.Model):
    name = models.CharField(max_length=20)
    seller = models.ForeignKey(User, verbose_name="seller")
    initial_price = models.DecimalField(max_digits=10, decimal_places = 2, verbose_name="starting bid" )
    description = models.TextField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, default= datetime.now())
    product_category = models.ForeignKey(ProductCategory, verbose_name="product category")

    def __unicode__(self):
        return smart_unicode(self.name)

    @classmethod
    def fetchOwnProducts(cls):
        try:
            queryset = cls.objects.all().order_by('-timestamp')
            return queryset
        except IndexError:
            return None


class AuctionStatus(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return smart_unicode(self.name)


class Auction(models.Model):
    title = models.CharField(max_length=20)
    current_price = models.DecimalField(max_digits=10, decimal_places = 2,
                                        null=True, blank=True, verbose_name="current bid" )
    updated_time = models.DateTimeField(auto_now_add=False,
                                        auto_now=True, default= datetime.now())
    end_time = models.DateTimeField()
    product = models.ForeignKey(Product)
    status = models.ForeignKey(AuctionStatus, verbose_name="auction status")

    def __unicode__(self):
        return smart_unicode(self.title)


    @classmethod
    def fetchLatestAuctions(cls):
        try:
            queryset = cls.objects.all().order_by('-end_time').reverse()[:10]
            return queryset
        except IndexError:
            return None


class Bidder(models.Model):
    contender = models.ForeignKey(User, verbose_name="contender")
    aucs = models.ManyToManyField(Auction, through='AuctionBidder')

    def __unicode__(self):
        return smart_unicode(self.contender)


class AuctionBidder(models.Model):
    contender = models.ForeignKey(Bidder)
    aucs = models.ForeignKey(Auction)
    bid_amount = models.DecimalField(max_digits=10, decimal_places = 2, verbose_name="bid amount" )
    bid_time = models.DateTimeField(auto_now_add=False,
                                        auto_now=True, default= datetime.now())

    def __unicode__(self):
        return smart_unicode(self.aucs)











