# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubhouse_contrib', '0007_auto_20160323_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asideblock',
            options={'ordering': ('order',), 'verbose_name': 'Aside Block', 'verbose_name_plural': 'Aside Blocks'},
        ),
        migrations.AlterModelOptions(
            name='contentblock',
            options={'ordering': ('order',), 'verbose_name': 'Content Block', 'verbose_name_plural': 'Content Blocks'},
        ),
    ]
