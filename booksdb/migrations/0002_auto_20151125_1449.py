# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booksdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinterestedgenres',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userbooks',
            name='book',
            field=models.ForeignKey(to='booksdb.Books'),
        ),
        migrations.AddField(
            model_name='userbooks',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='booksgenres',
            name='book',
            field=models.ForeignKey(to='booksdb.Books'),
        ),
        migrations.AddField(
            model_name='booksgenres',
            name='genre',
            field=models.ForeignKey(to='booksdb.Genres'),
        ),
        migrations.AlterUniqueTogether(
            name='userinterestedgenres',
            unique_together=set([('user', 'genre')]),
        ),
        migrations.AlterUniqueTogether(
            name='userbooks',
            unique_together=set([('user', 'book', 'quantity_no')]),
        ),
        migrations.AlterUniqueTogether(
            name='booksgenres',
            unique_together=set([('book', 'genre')]),
        ),
    ]
