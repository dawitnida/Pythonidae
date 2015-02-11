# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0004_auto_20141011_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 12, 0, 57, 42, 374000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 12, 0, 57, 42, 376000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 12, 0, 57, 42, 372000), auto_now_add=True),
        ),
    ]
