# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubhouse_contrib', '0009_auto_20160323_1724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contentblock',
            options={'verbose_name': 'Content Block', 'verbose_name_plural': 'Content Blocks'},
        ),
    ]
