from django.contrib import admin
from yaas.models import Auction, AuctionStatus, Product, Category

# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'product', 'auction_price', 'start_date', 'end_date', 'status', )
    search_fields = ['title']

    def owner(self, instance):
        return instance.user.username

    def auction_price(self, instance):
        return instance.product.price

    class Meta:
        model = Auction


class AuctionStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = AuctionStatus


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'category')
    search_fields = ['name', 'minimumPrice']

    class Meta:
        model = Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    class Meta:
        model = Category



admin.site.register(Auction, AuctionAdmin)
admin.site.register(AuctionStatus, AuctionStatusAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)


