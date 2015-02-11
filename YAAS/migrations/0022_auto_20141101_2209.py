# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0021_auto_20141024_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='product',
            field=models.OneToOneField(related_name=b'product', to='yaas.Product'),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='auc',
            field=models.ForeignKey(related_name=b'unique_auction', to='yaas.Auction'),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='unique_bidder',
            field=models.ForeignKey(related_name=b'unique_bidder', to='yaas.Bidder'),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='auctions',
            field=models.ManyToManyField(related_name=b'auctions', through='yaas.AuctionBidder', to=b'yaas.Auction'),
        ),
        migrations.AlterField(
            model_name='bidder',
            name='contender',
            field=models.ForeignKey(related_name=b'buyer', verbose_name=b'contender', to=settings.AUTH_USER_MODEL),
        ),
    ]
