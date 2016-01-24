# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0007_auto_20151128_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookfeedbackcomments',
            name='comment',
            field=models.TextField(),
        ),
    ]
