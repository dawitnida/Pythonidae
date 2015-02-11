# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0016_auto_20141021_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=b'2014-10-21 00:08:47', auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 21, 0, 8, 47, 264000), auto_now=True),
        ),
    ]
