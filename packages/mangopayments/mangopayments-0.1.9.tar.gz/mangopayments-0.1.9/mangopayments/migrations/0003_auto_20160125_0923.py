# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('mangopayments', '0002_mangopaypayin_result_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangopayrefund',
            name='debited_funds',
            field=models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='mangopayrefund',
            name='fees',
            field=models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2),
        ),
    ]
