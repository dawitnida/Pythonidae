""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 24.10.2014"
__version__ = "Version: "

from rest_framework import serializers

from yaas.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class AuctionSerializer(serializers.ModelSerializer):
    seller = serializers.RelatedField(source='product.seller')
    product_name = serializers.RelatedField(source='product')
    initial_price = serializers.RelatedField(source='product.initial_price')
    product_category = serializers.RelatedField(source='product.product_category')
    product_description = serializers.RelatedField(source='product.description')

    class Meta:
        model = Auction

        fields = ('product_name', 'title', 'initial_price', 'current_price', 'updated_time',
                  'end_time', 'product_category', 'product_description', 'seller', 'status')


class BidSerializer(serializers.ModelSerializer):
    seller = serializers.RelatedField(source='auc.product.seller')
    auc_title = serializers.RelatedField(source='auc.title')
    initial_price = serializers.RelatedField(source='auc.product.initial_price')

    class Meta:
        model = AuctionBidder
        fields = ('auc_title', 'seller', 'initial_price',
                  'unique_bidder', 'bid_amount', 'bid_time',  )


def validate_text(self, attrs, source):
    value = attrs[source]
    if len(value) < 5:
        raise serializers.ValidationError(
            "Text is too short."
        )
    return attrs

