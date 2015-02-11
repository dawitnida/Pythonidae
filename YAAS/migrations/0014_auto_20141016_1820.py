# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0013_auto_20141014_2340'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionbidder',
            old_name='aucs',
            new_name='auc',
        ),
        migrations.RenameField(
            model_name='bidder',
            old_name='aucs',
            new_name='auctions',
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 16, 18, 20, 49, 134000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 16, 18, 20, 49, 134000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
