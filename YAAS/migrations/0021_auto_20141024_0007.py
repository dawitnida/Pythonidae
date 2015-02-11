# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yaas', '0020_auto_20141023_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='end_time',
            field=models.DateTimeField(verbose_name=b'end time'),
        ),
    ]
