# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-07 15:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_auto_20180407_1523'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Applicant',
            new_name='User',
        ),
    ]