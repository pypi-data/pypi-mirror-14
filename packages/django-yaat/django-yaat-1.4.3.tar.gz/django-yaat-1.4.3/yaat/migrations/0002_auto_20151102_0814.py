# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('yaat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='user',
            field=models.ForeignKey(to=getattr(settings, 'YAAT_FOREIGN_KEY', settings.AUTH_USER_MODEL), verbose_name='User', related_name='columns'),
        ),
    ]
