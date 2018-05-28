# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-05-28 21:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=64)),
                ('last_name', models.CharField(blank=True, max_length=64)),
                ('phone_number', models.CharField(blank=True, max_length=16)),
                ('devpost', models.CharField(blank=True, max_length=64)),
                ('github', models.CharField(blank=True, max_length=64)),
                ('linkedin', models.CharField(blank=True, max_length=64)),
                ('personal_website', models.CharField(blank=True, max_length=128)),
                ('school', models.CharField(blank=True, max_length=64)),
                ('essay_helped', models.CharField(blank=True, max_length=700)),
                ('essay_project', models.CharField(blank=True, max_length=700)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('college_grad_year', models.CharField(blank=True, choices=[('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('other', 'Other')], max_length=4, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('no_answer', 'Prefer not to answer')], max_length=8, null=True)),
                ('major', models.CharField(blank=True, max_length=64)),
                ('current_study_level', models.CharField(blank=True, choices=[('high_school', 'High School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('other', 'Other')], max_length=8, null=True)),
                ('race_ethnicity', models.CharField(blank=True, choices=[('am_indian_or_ak_native', 'American Indian or Alaskan Native'), ('asian_or_pac_islander', 'Asian / Pacific Islander'), ('black_or_af_am', 'Black or African American'), ('hispanic', 'Hispanic'), ('white_caucasian', 'White / Caucasian'), ('multiple_or_other', 'Multiple ethnicity / Other'), ('no_answer', 'Prefer not to answer')], max_length=16, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='application', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('filename', models.CharField(blank=True, max_length=512)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resumes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('phone_number', models.CharField(max_length=16)),
                ('devpost', models.CharField(blank=True, max_length=64)),
                ('github', models.CharField(blank=True, max_length=64)),
                ('linkedin', models.CharField(blank=True, max_length=64)),
                ('personal_website', models.CharField(blank=True, max_length=128)),
                ('school', models.CharField(max_length=64)),
                ('essay_helped', models.CharField(blank=True, max_length=700)),
                ('essay_project', models.CharField(blank=True, max_length=700)),
                ('age', models.PositiveIntegerField()),
                ('college_grad_year', models.CharField(choices=[('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('other', 'Other')], max_length=4)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('no_answer', 'Prefer not to answer')], max_length=8)),
                ('major', models.CharField(max_length=64)),
                ('current_study_level', models.CharField(choices=[('high_school', 'High School'), ('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('other', 'Other')], max_length=8)),
                ('race_ethnicity', models.CharField(choices=[('am_indian_or_ak_native', 'American Indian or Alaskan Native'), ('asian_or_pac_islander', 'Asian / Pacific Islander'), ('black_or_af_am', 'Black or African American'), ('hispanic', 'Hispanic'), ('white_caucasian', 'White / Caucasian'), ('multiple_or_other', 'Multiple ethnicity / Other'), ('no_answer', 'Prefer not to answer')], max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='submissions', to='application.Application')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
