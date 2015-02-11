# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('updated_time', models.DateTimeField(default=datetime.datetime(2014, 10, 11, 1, 18, 21, 918000), auto_now=True)),
                ('end_time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuctionStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('initial_price', models.DecimalField(verbose_name=b'Starting Price', max_digits=10, decimal_places=2)),
                ('highest_price', models.DecimalField(null=True, verbose_name=b'Highest Price', max_digits=10, decimal_places=2, blank=True)),
                ('description', models.TextField(max_length=140)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2014, 10, 11, 1, 18, 21, 917000), auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.ForeignKey(verbose_name=b'Product Category', to='yaas.ProductCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(verbose_name=b'Owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='product',
            field=models.ForeignKey(to='yaas.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auction',
            name='status',
            field=models.ForeignKey(verbose_name=b'Auction Status', to='yaas.AuctionStatus'),
            preserve_default=True,
        ),
    ]
