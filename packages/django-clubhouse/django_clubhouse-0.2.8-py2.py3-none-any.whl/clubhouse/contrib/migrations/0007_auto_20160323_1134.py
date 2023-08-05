# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubhouse_contrib', '0006_auto_20160323_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_galleryblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='galleryblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_galleryblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='groupingblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_groupingblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='groupingblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_groupingblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='rowseparatorblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_rowseparatorblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='rowseparatorblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_rowseparatorblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='twitterfeedblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_twitterfeedblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='twitterfeedblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_twitterfeedblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='verticalspacingblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_verticalspacingblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='verticalspacingblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_verticalspacingblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='wysiwygblock',
            name='user_created',
            field=models.ForeignKey(related_name='clubhouse_contrib_wysiwygblock_blocks_created', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='wysiwygblock',
            name='user_updated',
            field=models.ForeignKey(related_name='clubhouse_contrib_wysiwygblock_blocks_updated', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
