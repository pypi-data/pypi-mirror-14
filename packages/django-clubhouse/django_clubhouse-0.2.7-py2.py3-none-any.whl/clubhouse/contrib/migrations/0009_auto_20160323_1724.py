# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubhouse_contrib', '0008_auto_20160323_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asideblock',
            name='additional_classes',
            field=models.CharField(help_text='Space separated list of additional css classes', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='additional_classes',
            field=models.CharField(help_text='Space separated list of additional css classes', max_length=255, null=True, blank=True),
        ),
    ]
