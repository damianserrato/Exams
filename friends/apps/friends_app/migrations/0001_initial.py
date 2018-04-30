# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-30 00:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('password', models.CharField(max_length=255)),
                ('confirm', models.CharField(max_length=255)),
            ],
        ),
    ]
