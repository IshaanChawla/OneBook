# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksdb', '0004_auto_20151127_1345'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookfeedbackrating',
            unique_together=set([('user', 'book')]),
        ),
    ]
