# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-29 01:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='college_grad_year',
            field=models.CharField(blank=True, choices=[('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('other', 'Other')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='college_grad_year',
            field=models.CharField(choices=[('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('other', 'Other')], max_length=8),
        ),
    ]
