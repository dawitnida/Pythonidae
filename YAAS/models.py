from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode
from django.core.validators import MinValueValidator


class ProductCategory(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        unique_together = (("name"),)

    def __unicode__(self):
        return smart_unicode(self.name)


class Product(models.Model):
    name = models.CharField(max_length=20)
    seller = models.ForeignKey(User, verbose_name="seller")
    initial_price = models.DecimalField(max_digits=10, decimal_places=2,
                                        validators=[MinValueValidator(0)], verbose_name="starting bid")
    description = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    product_category = models.ForeignKey(ProductCategory, verbose_name="product category")

    # class Meta:
    #   unique_together = (("name"),)

    def __unicode__(self):
        return smart_unicode(self.name)


class AuctionStatus(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        unique_together = (("name"),)

    def __unicode__(self):
        return smart_unicode(self.name)


class Auction(models.Model):
    title = models.CharField(max_length=20)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        null=True, blank=True, verbose_name="current bid")
    # now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updated_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    end_time = models.DateTimeField(verbose_name="end time")
    product = models.OneToOneField(Product)
    status = models.ForeignKey(AuctionStatus, verbose_name="auction status")

    class Meta:
        unique_together = (("title"),)
        ordering = ['end_time']

    def __unicode__(self):
        return smart_unicode(self.title)

    @classmethod
    def fetchActiveAuctions(cls):
        try:
            queryset = cls.objects.filter(status_id=1).order_by('-end_time').reverse()
            return queryset
        except IndexError:
            return None

    @classmethod
    def getAuctionByID(cls, aucid):
        try:
            return cls.objects.get(id=aucid, status_id=1)
        except IndexError:
            return None

    @classmethod
    def getAuctionByCategory(cls, catid):
        try:
            prodcat = Product.objects.filter(product_category=catid)
            queryset = Auction.objects.filter(product_id=prodcat, status_id=1)
            return queryset
        except IndexError:
            return None

    @classmethod
    def getAuctionByOwner(cls, ownerid):
        try:
            myprod = Product.objects.filter(seller_id=ownerid)
            queryset = Auction.objects.filter(product_id=myprod, status_id=1)
            return queryset
        except IndexError:
            return None

    @classmethod
    def getOwnerByAuctionID(cls, aucid):
        try:
            queryset = Auction.objects.get(id=aucid, status_id=1)
            myprod = Product.objects.get(id=queryset.product_id)
            seller = myprod.seller
            return seller
        except IndexError:
            return None

    @classmethod
    def getAuctionByProductID(cls, product_id):
        try:
            queryset = Auction.objects.get(product=product_id, status_id=1)
            return queryset
        except IndexError:
            return None


class Bidder(models.Model):
    contender = models.ForeignKey(User, verbose_name="contender")
    auctions = models.ManyToManyField(Auction, through='AuctionBidder')

    def __unicode__(self):
        return smart_unicode(self.contender)

    class Meta:
        ordering = ["contender"]


class AuctionBidder(models.Model):
    unique_bidder = models.ForeignKey(Bidder)
    auc = models.ForeignKey(Auction)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                     verbose_name="bid amount")
    bid_time = models.DateTimeField(auto_now_add=False, auto_now=True, )

    def __unicode__(self):
        return smart_unicode(self.auc)

    class Meta:
        ordering = ["bid_time"]




