# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20151130_0139'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_followed', models.ForeignKey(related_name='user_followed', to=settings.AUTH_USER_MODEL)),
                ('user_follower', models.ForeignKey(related_name='user_follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
