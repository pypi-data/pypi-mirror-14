# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubhouse_contrib', '0005_auto_20160311_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 2, 540957, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='galleryblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 5, 264742, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='galleryblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_galleryblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='galleryblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_galleryblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='groupingblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 7, 231195, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupingblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 9, 221784, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupingblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_groupingblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='groupingblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_groupingblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='rowseparatorblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 11, 776478, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rowseparatorblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 13, 852840, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rowseparatorblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_rowseparatorblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='rowseparatorblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_rowseparatorblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='twitterfeedblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 15, 435124, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterfeedblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 17, 891, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='twitterfeedblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_twitterfeedblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='twitterfeedblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_twitterfeedblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='verticalspacingblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 18, 493012, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verticalspacingblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 20, 149733, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verticalspacingblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_verticalspacingblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='verticalspacingblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_verticalspacingblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='wysiwygblock',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 21, 549690, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wysiwygblock',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 23, 11, 21, 23, 16322, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wysiwygblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_wysiwygblock_blocks_created', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='wysiwygblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_wysiwygblock_blocks_updated', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
