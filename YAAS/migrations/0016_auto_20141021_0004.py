# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0015_auto_20141017_0217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={'ordering': ['end_time']},
        ),
        migrations.AlterModelOptions(
            name='auctionbidder',
            options={'ordering': ['bid_time']},
        ),
        migrations.AlterModelOptions(
            name='bidder',
            options={'ordering': ['contender']},
        ),
        migrations.AlterField(
            model_name='auction',
            name='end_time',
            field=models.DateTimeField(verbose_name=b'%Y-%m-%d %H:%M:%S'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=b'2014-10-21 00:04:56', auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 21, 0, 4, 56, 490000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='initial_price',
            field=models.DecimalField(verbose_name=b'starting bid', max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
