# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0005_auto_20151127_1354'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookfeedbackrating',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='bookfeedbackrating',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookfeedbackrating',
            name='user',
        ),
        migrations.DeleteModel(
            name='BookFeedbackRating',
        ),
    ]
