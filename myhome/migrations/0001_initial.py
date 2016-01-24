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
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('house_number', models.CharField(max_length=30)),
                ('area', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('zip_code', models.CharField(max_length=6)),
                ('lat', models.DecimalField(default=0, max_digits=10, decimal_places=7)),
                ('lon', models.DecimalField(default=0, max_digits=10, decimal_places=7)),
                ('primary', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(null=True, blank=True)),
                ('date_read', models.DateTimeField(null=True, blank=True)),
                ('book', models.ForeignKey(to='booksdb.Books')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('send', models.BooleanField(default=False)),
                ('book_concerned', models.ForeignKey(to='booksdb.UserBooks', null=True)),
                ('user_reciever', models.ForeignKey(related_name='reciever', to=settings.AUTH_USER_MODEL)),
                ('user_sender', models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='notify',
            unique_together=set([('user_sender', 'user_reciever', 'timestamp')]),
        ),
        migrations.AlterUniqueTogether(
            name='booklist',
            unique_together=set([('user', 'book')]),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set([('user', 'house_number', 'area', 'city', 'state', 'zip_code')]),
        ),
    ]
