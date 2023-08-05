# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import localflavor.generic.models
import jsonfield.fields
from decimal import Decimal
import django_countries.fields
import django_filepicker.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MangoPayBankAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('address', models.CharField(default=b'', max_length=254)),
                ('city', models.CharField(default=b'', max_length=255)),
                ('postal_code', models.IntegerField(default=0)),
                ('region', models.CharField(max_length=255, null=True, blank=True)),
                ('country_code', models.CharField(default=b'', max_length=255)),
                ('account_type', models.CharField(default=b'BI', max_length=2, choices=[(b'BI', 'BIC & IBAN'), (b'US', 'Local US Format'), (b'O', 'Other')])),
                ('iban', localflavor.generic.models.IBANField(max_length=34, null=True, blank=True)),
                ('bic', localflavor.generic.models.BICField(max_length=11, null=True, blank=True)),
                ('account_number', models.CharField(max_length=15, null=True, blank=True)),
                ('aba', models.CharField(max_length=9, null=True, blank=True)),
                ('deposit_account_type', models.CharField(blank=True, max_length=8, null=True, choices=[(b'CHECKING', 'Checking'), (b'SAVINGS', 'Savings')])),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('expiration_date', models.CharField(max_length=4, null=True, blank=True)),
                ('alias', models.CharField(max_length=16, null=True, blank=True)),
                ('provider', models.CharField(max_length=255, null=True, blank=True)),
                ('type', models.CharField(max_length=255, null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_valid', models.NullBooleanField()),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='mangopay_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayCardRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('mangopay_card', models.OneToOneField(related_name='mangopay_card_registration', null=True, blank=True, to='mangopayments.MangoPayCard')),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('type', models.CharField(max_length=2, choices=[(b'IP', b'IDENTITY_PROOF'), (b'RP', b'REGISTRATION_PROOF'), (b'AA', b'ARTICLES_OF_ASSOCIATION'), (b'SD', b'SHAREHOLDER_DECLARATION'), (b'AP', b'ADDRESS_PROOF')])),
                ('status', models.CharField(blank=True, max_length=1, null=True, choices=[(b'C', b'CREATED'), (b'A', b'VALIDATION_ASKED'), (b'V', b'VALIDATED'), (b'R', b'REFUSED')])),
                ('refused_reason_message', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', django_filepicker.models.FPUrlField(max_length=255)),
                ('document', models.ForeignKey(related_name='mangopay_pages', to='mangopayments.MangoPayDocument')),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayPayIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('execution_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=9, null=True, choices=[(b'CREATED', 'The request is created but not processed.'), (b'SUCCEEDED', 'The request has been successfully processed.'), (b'FAILED', 'The request has failed.')])),
                ('debited_funds', models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
                ('fees', models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
                ('currency', models.CharField(default=b'EUR', max_length=255)),
                ('result_code', models.CharField(max_length=6, null=True, blank=True)),
                ('type', models.CharField(max_length=10, choices=[(b'bank-wire', 'Pay in by BankWire'), (b'card-web', 'Pay in by card via web')])),
                ('secure_mode_redirect_url', models.URLField(null=True, blank=True)),
                ('wire_reference', models.CharField(max_length=50, null=True, blank=True)),
                ('mangopay_bank_account', jsonfield.fields.JSONField(null=True, blank=True)),
                ('mangopay_card', models.ForeignKey(related_name='mangopay_payins', blank=True, to='mangopayments.MangoPayCard', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayPayOut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('execution_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=9, null=True, choices=[(b'CREATED', 'The request is created but not processed.'), (b'SUCCEEDED', 'The request has been successfully processed.'), (b'FAILED', 'The request has failed.')])),
                ('debited_funds', models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
                ('fees', models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
                ('currency', models.CharField(default=b'EUR', max_length=255)),
                ('mangopay_bank_account', models.ForeignKey(related_name='mangopay_payouts', to='mangopayments.MangoPayBankAccount')),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayRefund',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('execution_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=9, null=True, choices=[(b'CREATED', 'The request is created but not processed.'), (b'SUCCEEDED', 'The request has been successfully processed.'), (b'FAILED', 'The request has failed.')])),
                ('result_code', models.CharField(max_length=6, null=True, blank=True)),
                ('mangopay_pay_in', models.ForeignKey(related_name='mangopay_refunds', to='mangopayments.MangoPayPayIn')),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayTransfer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('debited_funds', models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
                ('fees', models.DecimalField(default=Decimal('0.0'), max_digits=12, decimal_places=2)),
                ('currency', models.CharField(default=b'EUR', max_length=255)),
                ('execution_date', models.DateTimeField(null=True, blank=True)),
                ('status', models.CharField(blank=True, max_length=9, null=True, choices=[(b'CREATED', 'The request is created but not processed.'), (b'SUCCEEDED', 'The request has been successfully processed.'), (b'FAILED', 'The request has failed.')])),
                ('result_code', models.CharField(max_length=6, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_edit_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('type', models.CharField(max_length=1, null=True, choices=[(b'N', 'Natural User'), (b'B', b'BUSINESS'), (b'O', b'ORGANIZATION')])),
                ('first_name', models.CharField(max_length=99, null=True, blank=True)),
                ('last_name', models.CharField(max_length=99, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('country_of_residence', django_countries.fields.CountryField(max_length=2)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('address', models.CharField(max_length=254, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('region', models.CharField(max_length=255, null=True, blank=True)),
                ('postal_code', models.IntegerField(default=0, null=True, blank=True)),
                ('country_code', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayWallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mangopay_id', models.PositiveIntegerField(null=True, blank=True)),
                ('currency', models.CharField(default=b'EUR', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='MangoPayLegalUser',
            fields=[
                ('mangopayuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mangopayments.MangoPayUser')),
                ('business_name', models.CharField(max_length=254)),
                ('generic_business_email', models.EmailField(max_length=254)),
                ('headquarters_address', models.CharField(max_length=254, null=True, blank=True)),
                ('headquarters_city', models.CharField(max_length=255, null=True, blank=True)),
                ('headquarters_region', models.CharField(max_length=255, null=True, blank=True)),
                ('headquarters_postal_code', models.IntegerField(default=0, null=True, blank=True)),
                ('headquarters_country_code', models.CharField(max_length=255, null=True, blank=True)),
            ],
            bases=('mangopayments.mangopayuser',),
        ),
        migrations.CreateModel(
            name='MangoPayNaturalUser',
            fields=[
                ('mangopayuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mangopayments.MangoPayUser')),
                ('occupation', models.CharField(max_length=254, null=True, blank=True)),
                ('income_range', models.SmallIntegerField(blank=True, null=True, choices=[(1, b'0 - 1,500'), (2, b'1,500 - 2,499'), (3, b'2,500 - 3,999'), (4, b'4,000 - 7,499'), (5, b'7,500 - 9,999'), (6, b'10,000 +')])),
            ],
            bases=('mangopayments.mangopayuser',),
        ),
        migrations.AddField(
            model_name='mangopaywallet',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_wallets', to='mangopayments.MangoPayUser'),
        ),
        migrations.AddField(
            model_name='mangopayuser',
            name='user',
            field=models.ForeignKey(related_name='mangopay_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mangopaytransfer',
            name='mangopay_credited_wallet',
            field=models.ForeignKey(related_name='mangopay_credited_wallets', to='mangopayments.MangoPayWallet'),
        ),
        migrations.AddField(
            model_name='mangopaytransfer',
            name='mangopay_debited_wallet',
            field=models.ForeignKey(related_name='mangopay_debited_wallets', to='mangopayments.MangoPayWallet'),
        ),
        migrations.AddField(
            model_name='mangopayrefund',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_refunds', to='mangopayments.MangoPayUser'),
        ),
        migrations.AddField(
            model_name='mangopaypayout',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_payouts', to='mangopayments.MangoPayUser'),
        ),
        migrations.AddField(
            model_name='mangopaypayout',
            name='mangopay_wallet',
            field=models.ForeignKey(related_name='mangopay_payouts', to='mangopayments.MangoPayWallet'),
        ),
        migrations.AddField(
            model_name='mangopaypayin',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_payins', to='mangopayments.MangoPayUser'),
        ),
        migrations.AddField(
            model_name='mangopaypayin',
            name='mangopay_wallet',
            field=models.ForeignKey(related_name='mangopay_payins', to='mangopayments.MangoPayWallet'),
        ),
        migrations.AddField(
            model_name='mangopaydocument',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_documents', to='mangopayments.MangoPayUser'),
        ),
        migrations.AddField(
            model_name='mangopaycardregistration',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_card_registrations', to='mangopayments.MangoPayUser'),
        ),
        migrations.AddField(
            model_name='mangopaybankaccount',
            name='mangopay_user',
            field=models.ForeignKey(related_name='mangopay_bank_accounts', to='mangopayments.MangoPayUser'),
        ),
        migrations.CreateModel(
            name='MangoPayPayInBankWire',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('mangopayments.mangopaypayin',),
        ),
        migrations.CreateModel(
            name='MangoPayPayInByCard',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('mangopayments.mangopaypayin',),
        ),
    ]
