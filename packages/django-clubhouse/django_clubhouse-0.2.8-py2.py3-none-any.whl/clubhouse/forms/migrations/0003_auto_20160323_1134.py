# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubhouse_forms', '0002_auto_20160323_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_forms_formblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='formblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_forms_formblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
