# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0009_auto_20151129_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookfeedbackrate',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
