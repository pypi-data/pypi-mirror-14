# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubhouse_forms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='formblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 24, 587114, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 26, 93014, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_forms_formblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='formblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_forms_formblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
