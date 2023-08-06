# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubhouse_contrib', '0010_auto_20160330_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryblock',
            name='zip_import',
            field=models.FileField(help_text="Upload a zip file containing images, and they'll be imported into this gallery.", upload_to='galleries', verbose_name='Zip import', blank=True),
        ),
    ]
