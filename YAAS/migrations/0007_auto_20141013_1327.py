# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0006_auto_20141012_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='product',
            field=models.OneToOneField(to='yaas.Product'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 13, 13, 27, 18, 749000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 13, 13, 27, 18, 754000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 13, 13, 27, 18, 744000), auto_now_add=True),
        ),
    ]
