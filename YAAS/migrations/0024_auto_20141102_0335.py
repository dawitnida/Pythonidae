# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import concurrency.fields


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0023_auctionstatus_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=1, help_text='record revision number'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auctionbidder',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=1, help_text='record revision number'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bidder',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=1, help_text='record revision number'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=1, help_text='record revision number'),
            preserve_default=True,
        ),
    ]
