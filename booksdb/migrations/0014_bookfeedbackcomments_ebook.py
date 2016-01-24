# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0013_auto_20151202_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookfeedbackcomments',
            name='ebook',
            field=models.FileField(null=True, upload_to=b'ebooks/', blank=True),
        ),
    ]
