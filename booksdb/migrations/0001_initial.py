# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('isbn', models.CharField(max_length=13, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('author', models.CharField(max_length=40)),
                ('pub_status', models.CharField(default=b'Yes', max_length=10)),
                ('avg_rating', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('goodread_avg_rating', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('language', models.CharField(default=b'English', max_length=15)),
                ('description', models.TextField(default=b'No Description Available')),
                ('book_pic', models.ImageField(null=True, upload_to=b'book_pics/')),
            ],
        ),
        migrations.CreateModel(
            name='BooksGenres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('genre_id', models.AutoField(serialize=False, primary_key=True)),
                ('genre_name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='UserBooks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity_no', models.IntegerField()),
                ('health', models.DecimalField(default=0, max_digits=3, decimal_places=2)),
                ('avail', models.BooleanField(default=True)),
                ('moe', models.CharField(default=b'te', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='UserInterestedGenres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.ForeignKey(to='booksdb.Genres')),
            ],
        ),
    ]
