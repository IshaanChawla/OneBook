# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booksdb', '0003_auto_20151127_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookFeedbackComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(max_length=500)),
                ('book', models.ForeignKey(to='booksdb.Books')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookFeedbackRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(to='booksdb.Books')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='bookfeedback',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='bookfeedback',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookfeedback',
            name='user',
        ),
        migrations.DeleteModel(
            name='BookFeedback',
        ),
        migrations.AlterUniqueTogether(
            name='bookfeedbackcomments',
            unique_together=set([('user', 'book', 'timestamp')]),
        ),
    ]
