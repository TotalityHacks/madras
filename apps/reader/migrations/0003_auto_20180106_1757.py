# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-06 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0002_auto_20171113_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingfield',
            name='options',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='ratingfield',
            name='type',
            field=models.CharField(choices=[('numerical', 'Numerical'), ('multiple_choice', 'Multiple choice')], max_length=16),
        ),
    ]