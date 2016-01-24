# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booksdb', '0002_auto_20151125_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=500)),
                ('rating', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('book', models.ForeignKey(to='booksdb.Books')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bookfeedback',
            unique_together=set([('user', 'book', 'timestamp')]),
        ),
    ]
