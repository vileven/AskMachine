# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]