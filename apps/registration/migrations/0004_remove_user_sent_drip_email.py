# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-08 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_user_sent_drip_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sent_drip_email',
        ),
    ]
