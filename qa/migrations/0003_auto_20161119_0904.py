# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 09:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0002_profile_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatar/avatar/default-user-image.png', null=True, upload_to='avatar/'),
        ),
    ]