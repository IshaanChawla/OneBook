# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0014_bookfeedbackcomments_ebook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookfeedbackcomments',
            name='ebook',
        ),
        migrations.AddField(
            model_name='userbooks',
            name='ebook',
            field=models.FileField(null=True, upload_to=b'ebooks/', blank=True),
        ),
    ]
