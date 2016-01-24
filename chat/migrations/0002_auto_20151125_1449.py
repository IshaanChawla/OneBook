# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatline',
            name='user_one',
            field=models.ForeignKey(related_name='user_one', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatline',
            name='user_two',
            field=models.ForeignKey(related_name='user_two', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='textmessage',
            unique_together=set([('chat', 'timestamp')]),
        ),
    ]
