# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mangopayments', '0006_mangopaybankaccount_owner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='mangopaypayout',
            name='bank_wire_ref',
            field=models.CharField(default=b'', max_length=12, null=True, blank=True),
        ),
    ]
