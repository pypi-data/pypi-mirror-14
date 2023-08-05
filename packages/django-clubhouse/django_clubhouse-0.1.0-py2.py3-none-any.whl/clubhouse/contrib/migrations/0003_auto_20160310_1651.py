# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('clubhouse_contrib', '0002_auto_20160225_1254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageasideblock',
            name='page',
        ),
        migrations.RemoveField(
            model_name='pagecontentblock',
            name='page',
        ),
        migrations.AddField(
            model_name='groupcontentblock',
            name='page_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='groupcontentblock',
            name='page_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_groupcontentblock_page', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='pageasideblock',
            name='page_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pageasideblock',
            name='page_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_pageasideblock_page', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='pagecontentblock',
            name='page_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pagecontentblock',
            name='page_type',
            field=models.ForeignKey(related_name='clubhouse_contrib_pagecontentblock_page', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='contenttypes.ContentType', null=True),
        ),
    ]
