# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20150527_1555'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('can_reuse', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Gallery',
                'verbose_name_plural': 'Gallery',
            },
        ),
        migrations.CreateModel(
            name='GalleryBlockImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('file', mezzanine.core.fields.FileField(max_length=200, verbose_name='File')),
                ('description', models.CharField(max_length=1000, verbose_name='Description', blank=True)),
                ('block', models.ForeignKey(related_name='images', to='clubhouse_contrib.GalleryBlock')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.CreateModel(
            name='GroupContentBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.CharField(default='m', max_length=1, null=True, blank=True, choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('f', 'Span')])),
                ('block_id', models.PositiveIntegerField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('additional_classes', models.CharField(max_length=255, null=True, blank=True)),
                ('block_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Grouping Content Block',
                'verbose_name_plural': 'Grouping Content Blocks',
            },
        ),
        migrations.CreateModel(
            name='GroupingBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('can_reuse', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Block Group',
                'verbose_name_plural': 'Block Grouping',
            },
        ),
        migrations.CreateModel(
            name='ModularPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='pages.Page')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Modular Page',
            },
            bases=('pages.page',),
        ),
        migrations.CreateModel(
            name='PageAsideBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block_id', models.PositiveIntegerField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('additional_classes', models.CharField(max_length=255, null=True, blank=True)),
                ('block_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('page', models.ForeignKey(related_name='aside_blocks', to='clubhouse_contrib.ModularPage')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Page Aside Block',
                'verbose_name_plural': 'Page Aside Blocks',
            },
        ),
        migrations.CreateModel(
            name='PageContentBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('size', models.CharField(default='m', max_length=1, null=True, blank=True, choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('f', 'Span')])),
                ('block_id', models.PositiveIntegerField(null=True, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('additional_classes', models.CharField(max_length=255, null=True, blank=True)),
                ('block_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('page', models.ForeignKey(related_name='content_blocks', to='clubhouse_contrib.ModularPage')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Page Content Block',
                'verbose_name_plural': 'Page Content Blocks',
            },
        ),
        migrations.CreateModel(
            name='RowSeparatorBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Row Separator',
                'verbose_name_plural': 'Row Separators',
            },
        ),
        migrations.CreateModel(
            name='TwitterFeedBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('can_reuse', models.BooleanField(default=False)),
                ('twitter_query', models.ForeignKey(to='twitter.Query')),
            ],
            options={
                'verbose_name': 'Twitter Feed',
                'verbose_name_plural': 'Twitter Feeds',
            },
        ),
        migrations.CreateModel(
            name='VerticalSpacingBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('height', models.CharField(default='10rem', max_length=10)),
            ],
            options={
                'verbose_name': 'Spacer',
                'verbose_name_plural': 'Spacers',
            },
        ),
        migrations.CreateModel(
            name='WysiwygBlock',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('can_reuse', models.BooleanField(default=False)),
                ('content', mezzanine.core.fields.RichTextField(verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Rich Text',
                'verbose_name_plural': 'Rich Text',
            },
        ),
        migrations.AddField(
            model_name='groupcontentblock',
            name='group',
            field=models.ForeignKey(related_name='content_blocks', to='clubhouse_contrib.GroupingBlock'),
        ),
    ]
