# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0019_auto_20141023_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
