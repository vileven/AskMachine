# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 12:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20161119_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me',
            field=models.TextField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='default-user-image.png', null=True, upload_to='avatar/'),
        ),
    ]
