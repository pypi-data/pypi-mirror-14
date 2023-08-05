# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangopayments', '0005_auto_20160311_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangopaybankaccount',
            name='owner_name',
            field=models.CharField(default=b'', max_length=255),
        ),
    ]
