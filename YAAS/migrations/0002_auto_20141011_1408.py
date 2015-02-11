# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yaas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionBidder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bid_amount', models.DecimalField(verbose_name=b'bid amount', max_digits=10, decimal_places=2)),
                ('bid_time', models.DateTimeField(default=datetime.datetime(2014, 10, 11, 14, 8, 33, 587000), auto_now=True)),
                ('aucs', models.ForeignKey(to='yaas.Auction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bidder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aucs', models.ManyToManyField(to='yaas.Auction', through='yaas.AuctionBidder')),
                ('contender', models.ForeignKey(verbose_name=b'contender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='auctionbidder',
            name='contender',
            field=models.ForeignKey(to='yaas.Bidder'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='product',
            name='highest_price',
        ),
        migrations.AddField(
            model_name='auction',
            name='current_price',
            field=models.DecimalField(null=True, verbose_name=b'current bid', max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.ForeignKey(verbose_name=b'auction status', to='yaas.AuctionStatus'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 11, 14, 8, 33, 587000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='initial_price',
            field=models.DecimalField(verbose_name=b'starting bid', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(verbose_name=b'product category', to='yaas.ProductCategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 11, 14, 8, 33, 587000), auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(verbose_name=b'seller', to=settings.AUTH_USER_MODEL),
        ),
    ]
