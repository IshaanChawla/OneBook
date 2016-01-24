# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_followuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2015, 12, 2)),
        ),
        migrations.AlterUniqueTogether(
            name='followuser',
            unique_together=set([('user_followed', 'user_follower')]),
        ),
    ]
