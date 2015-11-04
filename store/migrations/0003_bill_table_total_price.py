# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20150128_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_table',
            name='total_price',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
