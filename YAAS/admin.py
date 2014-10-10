from django.contrib import admin
from yaas.models import Auction, AuctionStatus, Product, ProductCategory

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product', 'auction_category','user',
                    'starting_price', 'highest_bid_price', 'updated_time', 'end_time', 'status', )
    search_fields = ['title']

    def starting_price(self, instance):
        return instance.product.initial_price

    def highest_bid_price(self, instance):
        return instance.product.highest_price

    def auction_category(self, instance):
        return instance.product.product_category

    class Meta:
        model = Auction


class AuctionStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = AuctionStatus


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'timestamp','initial_price', 'highest_price', 'description', 'product_category')
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


