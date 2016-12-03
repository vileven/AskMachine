# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 13:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(null=True, upload_to='/avatar/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.IntegerField(default=0)),
                ('count_answers', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_author', to='qa.Profile')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='question_dislike', to='qa.Profile')),
                ('likes', models.ManyToManyField(blank=True, related_name='question_like', to='qa.Profile')),
            ],
            options={
                'ordering': ('-added_at',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('counts', models.PositiveIntegerField(default=0)),
                ('question', models.ManyToManyField(blank=True, to='qa.Question')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_author', to='qa.Profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='answer_dislikes', to='qa.Profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='answer_likes', to='qa.Profile'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.Question'),
        ),
    ]