# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('yaas', '0009_auto_20141013_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 14, 22, 32, 1, 43000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='auctionbidder',
            name='bid_time',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 14, 22, 32, 1, 43000), auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=280),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 14, 22, 32, 1, 43000), auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='auction',
            unique_together=set([('title',)]),
        ),
        migrations.AlterUniqueTogether(
            name='auctionstatus',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='productcategory',
            unique_together=set([('name',)]),
        ),
    ]
