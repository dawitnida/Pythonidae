# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0014_auto_20141016_1820'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionbidder',
            old_name='contender',
            new_name='unique_bidder',
        ),
        migrations.AlterField(
            model_name='auction',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, null=True, verbose_name=b'current bid'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 17, 2, 17, 10, 189000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 17, 2, 17, 10, 189000), auto_now=True),
        ),
    ]
