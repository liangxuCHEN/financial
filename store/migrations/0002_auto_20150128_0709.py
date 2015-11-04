# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_table',
            name='bill_id',
        ),
        migrations.AddField(
            model_name='bill',
            name='bill_table',
            field=models.ForeignKey(default=1, to='store.Bill_table'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_comment',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bill_table',
            name='comment',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
