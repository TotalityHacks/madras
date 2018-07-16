# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-06-07 02:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20180531_2118'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reader', '0002_skip'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='skip',
            unique_together=set([('application', 'user')]),
        ),
    ]
