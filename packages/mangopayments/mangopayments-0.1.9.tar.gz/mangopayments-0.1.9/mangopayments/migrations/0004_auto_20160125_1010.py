# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangopayments', '0003_auto_20160125_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mangopayrefund',
            name='execution_date',
        ),
        migrations.AddField(
            model_name='mangopayrefund',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='mangopayrefund',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
