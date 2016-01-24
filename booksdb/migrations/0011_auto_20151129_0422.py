# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0010_auto_20151129_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='times_rated',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='books',
            name='total_rating',
            field=models.IntegerField(default=0),
        ),
    ]
