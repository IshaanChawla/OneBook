# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booksdb', '0008_auto_20151128_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookFeedbackRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('book', models.ForeignKey(to='booksdb.Books')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bookfeedbackrate',
            unique_together=set([('user', 'book')]),
        ),
    ]
