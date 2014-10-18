from django.contrib import admin
from django.contrib.auth.models import User
from yaas.models import Auction, AuctionStatus, Product
from .models import ProductCategory, AuctionBidder, Bidder


# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product', 'auction_category',
                    'starting_price', 'current_price', 'updated_time', 'end_time', 'status', )
    search_fields = ['title']

    def starting_price(self, instance):
        return instance.product.initial_price

    def auction_category(self, instance):
        return instance.product.product_category

    class Meta:
        model = Auction


class AuctionStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = AuctionStatus


class BidderAdmin(admin.ModelAdmin):
    list_display = ('id', 'contender', )

    class Meta:
        model = Bidder


class AuctionBidderAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique_bidder', 'auc', 'bid_amount', 'bid_time')

    class Meta:
        model = AuctionBidder


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','seller', 'timestamp','initial_price', 'description', 'product_category')
    search_fields = ['name']

    class Meta:
        model = Product

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = ProductCategory


admin.site.register(Auction, AuctionAdmin)
admin.site.register(AuctionStatus, AuctionStatusAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Bidder, BidderAdmin)
admin.site.register(AuctionBidder, AuctionBidderAdmin)


