# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('usercategories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangofeeds', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('active', models.BooleanField(default=True)),
                ('categories', models.ManyToManyField(to='usercategories.Category', null=True)),
                ('feed', models.ForeignKey(to='djangofeeds.Feed')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserFeedEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=0, choices=[(0, 'new'), (2, 'unread'), (4, 'read'), (3, 'seen'),
                                                                   (1, 'remember')])),
                ('rank', models.IntegerField(default=0)),
                ('entry', models.ForeignKey(to='djangofeeds.Post')),
                ('feed', models.ForeignKey(to='userfeeds.UserFeed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
