# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0012_auto_20141014_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccount',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserAccount',
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 14, 23, 40, 8, 90000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 14, 23, 40, 8, 92000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 14, 23, 40, 8, 89000), auto_now_add=True),
        ),
    ]
