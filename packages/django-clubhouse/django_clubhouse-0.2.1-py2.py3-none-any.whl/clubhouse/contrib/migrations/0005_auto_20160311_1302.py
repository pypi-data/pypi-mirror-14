# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('clubhouse_contrib', '0004_auto_20160310_1749'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupingBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('can_reuse', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Block Group',
                'verbose_name_plural': 'Block Grouping',
            },
        ),
        migrations.RenameField(
            model_name='asideblock',
            old_name='page_id',
            new_name='parent_id',
        ),
        migrations.RenameField(
            model_name='contentblock',
            old_name='page_id',
            new_name='parent_id',
        ),
        migrations.RemoveField(
            model_name='asideblock',
            name='page_type',
        ),
        migrations.RemoveField(
            model_name='contentblock',
            name='page_type',
        ),
        migrations.AddField(
            model_name='asideblock',
            name='parent_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_asideblock_parent', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='contentblock',
            name='parent_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_contentblock_parent', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='asideblock',
            name='block_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_asideblock_block', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AlterField(
            model_name='contentblock',
            name='block_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_contentblock_block', blank=True, to='contenttypes.ContentType', null=True),
        ),
    ]
