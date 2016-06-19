# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-18 12:36
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
                ('name', models.CharField(db_index=True, max_length=30, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email')),
            ],
        ),
    ]
