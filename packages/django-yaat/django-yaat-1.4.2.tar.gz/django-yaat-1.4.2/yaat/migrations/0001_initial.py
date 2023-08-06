# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('resource', models.CharField(max_length=64, verbose_name='Resource name')),
                ('key', models.CharField(max_length=64, verbose_name='Column key')),
                ('is_shown', models.NullBooleanField(verbose_name='Show field', default=True)),
                ('ordering', models.PositiveSmallIntegerField(choices=[(None, 'Ordering disallowed'), (0, 'Unordered'), (1, 'Ascending'), (2, 'Descending')], null=True, verbose_name='Field order', default=0)),
                ('is_virtual', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User', related_name='column_users')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='column',
            unique_together=set([('resource', 'user', 'key')]),
        ),
    ]
