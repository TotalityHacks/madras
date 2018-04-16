# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-04-16 18:30
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkingroup',
            name='id',
        ),
        migrations.AddField(
            model_name='checkingroup',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
