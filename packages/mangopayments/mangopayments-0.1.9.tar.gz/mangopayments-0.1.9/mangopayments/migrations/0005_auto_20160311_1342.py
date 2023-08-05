# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangopayments', '0004_auto_20160125_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangopaycard',
            name='alias',
            field=models.CharField(max_length=19, null=True, blank=True),
        ),
    ]
