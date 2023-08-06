# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enquiry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=200, db_index=True)),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('sent', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ('-sent',),
                'db_table': 'enquiries_enquiry',
                'verbose_name_plural': 'enquiries',
                'get_latest_by': 'sent',
            },
        ),
    ]
