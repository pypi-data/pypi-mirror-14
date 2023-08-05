# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    replaces = [('payplug_dj', '0001_initial'), ('payplug_dj', '0002_payment_payplug_url'), ('payplug_dj', '0003_auto_20160316_1749'), ('payplug_dj', '0004_auto_20160318_1543'), ('payplug_dj', '0005_auto_20160319_0559')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('email', models.CharField(verbose_name='email', max_length=50)),
                ('firstname', models.CharField(verbose_name='Firstname', max_length=50)),
                ('lastname', models.CharField(verbose_name='Lastname', max_length=50)),
                ('uuid', models.UUIDField(default=uuid.uuid4, verbose_name='UUID for transactions', unique=True, editable=False)),
                ('amount', models.FloatField(default=0, verbose_name='Amount')),
                ('currency', models.CharField(default='EUR', verbose_name='Currency', max_length=10)),
                ('payplug_id', models.CharField(default='', verbose_name='PayPlug transaction ID', null=True, max_length=150, blank=True)),
                ('state', models.CharField(default='W', verbose_name='Payment state', choices=[('C', 'Canceled'), ('P', 'Paid'), ('R', 'Refund'), ('W', 'Wait for payment')], max_length=1)),
                ('payplug_url', models.CharField(default='', verbose_name='PayPlug transaction URL', null=True, max_length=150, blank=True)),
                ('template_cancel', models.CharField(default='', verbose_name='Cancel template name', null=True, max_length=150, blank=True)),
                ('template_return', models.CharField(default='', verbose_name='Return template name', null=True, max_length=150, blank=True)),
            ],
        ),
    ]
