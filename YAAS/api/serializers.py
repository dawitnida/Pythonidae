""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 24.10.2014"
__version__ = "Version: "

from rest_framework import serializers

from yaas.models import *


# Model serializer class for auction bid view
# A bit of validation is done here
class AuctionBidderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionBidder

    def validate(self, attrs):
        auc = attrs['auc']
        initial_price = float(auc.product.initial_price)
        current_price = float(auc.current_price)
        bid_amount = float(attrs['bid_amount'])
        if (bid_amount > initial_price + 0.01) and (bid_amount > current_price + 0.01):
            auc.current_price = bid_amount  # Update the current highest price and may be in the future delete the auction itself
            auc.save(update_fields=['current_price'])
            return attrs
        else:
            raise serializers.ValidationError({"bid_amount_error": "Invalid bid amount."})


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionStatus


class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer()
    product_category = CategorySerializer()

    class Meta:
        model = Product


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction


class AuctionModelSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Makes life easier by just calling serialized related models
    status = StatusSerializer()

    class Meta:
        model = Auction


class AuctionBidderModelSerializer(serializers.ModelSerializer):
    aucs = AuctionSerializer()
    current_price = serializers.Field(source='current_price')
    end_time = serializers.Field(source='end_time')
    seller = serializers.RelatedField(source='product.seller')
    product_name = serializers.RelatedField(source='product.name')
    initial_price = serializers.RelatedField(source='product.initial_price')
    product_category = serializers.RelatedField(source='product.product_category')
    title = serializers.Field(source='title')

    class Meta:
        model = AuctionBidder
        fields = ('title', 'product_name', 'initial_price', 'current_price',
                  'end_time', 'product_category', 'seller',)
