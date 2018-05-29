# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-29 01:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20180529_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='current_study_level',
            field=models.CharField(blank=True, choices=[('high_school', 'High School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('other', 'Other')], max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='race_ethnicity',
            field=models.CharField(blank=True, choices=[('am_indian_or_ak_native', 'American Indian or Alaskan Native'), ('asian_or_pac_islander', 'Asian / Pacific Islander'), ('black_or_af_am', 'Black or African American'), ('hispanic', 'Hispanic'), ('white_caucasian', 'White / Caucasian'), ('multiple_or_other', 'Multiple ethnicity / Other'), ('no_answer', 'Prefer not to answer')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='current_study_level',
            field=models.CharField(choices=[('high_school', 'High School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('other', 'Other')], max_length=16),
        ),
        migrations.AlterField(
            model_name='submission',
            name='race_ethnicity',
            field=models.CharField(choices=[('am_indian_or_ak_native', 'American Indian or Alaskan Native'), ('asian_or_pac_islander', 'Asian / Pacific Islander'), ('black_or_af_am', 'Black or African American'), ('hispanic', 'Hispanic'), ('white_caucasian', 'White / Caucasian'), ('multiple_or_other', 'Multiple ethnicity / Other'), ('no_answer', 'Prefer not to answer')], max_length=32),
        ),
    ]
