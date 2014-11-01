from django.contrib import admin

from yaas.models import *


# Models are registered here.
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
    search_fields = ['contender__username']

    class Meta:
        model = Bidder


class AuctionBidderAdmin(admin.ModelAdmin):
    list_display = ('id', 'unique_bidder', 'auc', 'bid_amount', 'bid_time')
    search_fields = ['auc__title']

    class Meta:
        model = AuctionBidder


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'timestamp', 'initial_price', 'description', 'product_category')
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


