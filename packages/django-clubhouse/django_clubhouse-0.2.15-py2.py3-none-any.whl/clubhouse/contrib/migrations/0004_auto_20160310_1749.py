# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('clubhouse_contrib', '0003_auto_20160310_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsideBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block_id', models.PositiveIntegerField(null=True, blank=True)),
                ('page_id', models.PositiveIntegerField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('additional_classes', models.CharField(max_length=255, null=True, blank=True)),
                ('block_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('page_type', models.ForeignKey(related_name='clubhouse_contrib_asideblock_page', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Page Aside Block',
                'verbose_name_plural': 'Page Aside Blocks',
            },
        ),
        migrations.CreateModel(
            name='ContentBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block_id', models.PositiveIntegerField(null=True, blank=True)),
                ('page_id', models.PositiveIntegerField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('additional_classes', models.CharField(max_length=255, null=True, blank=True)),
                ('size', models.CharField(default='m', max_length=1, null=True, blank=True, choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('f', 'Span')])),
                ('block_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('page_type', models.ForeignKey(related_name='clubhouse_contrib_contentblock_page', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Page Content Block',
                'verbose_name_plural': 'Page Content Blocks',
            },
        ),
        migrations.RemoveField(
            model_name='groupcontentblock',
            name='block_type',
        ),
        migrations.RemoveField(
            model_name='groupcontentblock',
            name='group',
        ),
        migrations.RemoveField(
            model_name='groupcontentblock',
            name='page_type',
        ),
        migrations.RemoveField(
            model_name='pageasideblock',
            name='block_type',
        ),
        migrations.RemoveField(
            model_name='pageasideblock',
            name='page_type',
        ),
        migrations.RemoveField(
            model_name='pagecontentblock',
            name='block_type',
        ),
        migrations.RemoveField(
            model_name='pagecontentblock',
            name='page_type',
        ),
        migrations.DeleteModel(
            name='GroupContentBlock',
        ),
        migrations.DeleteModel(
            name='GroupingBlock',
        ),
        migrations.DeleteModel(
            name='PageAsideBlock',
        ),
        migrations.DeleteModel(
            name='PageContentBlock',
        ),
    ]
