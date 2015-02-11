# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0008_auto_20141013_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 13, 23, 17, 9, 321000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 13, 23, 17, 9, 322000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 13, 23, 17, 9, 319000), auto_now_add=True),
        ),
    ]
