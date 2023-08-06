# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from string import punctuation
import os
from chardet import detect as charsetdetect
from zipfile import ZipFile
from io import BytesIO

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from mezzanine.core import fields as mezzanine_fields
from mezzanine.core.models import Orderable
from mezzanine.utils.models import upload_to
from mezzanine.twitter.models import Query as TwitterQuery
from mezzanine.conf import settings
from mezzanine.utils.importing import import_dotted_path

from clubhouse.core.models import (
    BlockBase, ReusableBlock, AbstractModularComponent
)
from clubhouse.contrib.models.types import ContentBlock, AsideBlock

__all__ = ['GroupingBlock','WysiwygBlock','GalleryBlock',
    'GalleryBlockImage','VerticalSpacingBlock','TwitterFeedBlock',
    'RowSeparatorBlock']

# Set the directory where gallery images are uploaded to,
# either MEDIA_ROOT + 'galleries', or filebrowser's upload
# directory if being used.
GALLERIES_UPLOAD_DIR = "galleries"
if settings.PACKAGE_NAME_FILEBROWSER in settings.INSTALLED_APPS:
    fb_settings = "%s.settings" % settings.PACKAGE_NAME_FILEBROWSER
    try:
        GALLERIES_UPLOAD_DIR = import_dotted_path(fb_settings).DIRECTORY
    except ImportError:
        pass

class GroupingBlock(ReusableBlock, AbstractModularComponent):
    block_contexts = (ContentBlock, AsideBlock)

    class Meta:
        verbose_name = 'Block Group'
        verbose_name_plural = 'Block Grouping'

    @property
    def content(self):
        return self.get_blocks_by_context(ContentBlock)


class WysiwygBlock(ReusableBlock):
    content = mezzanine_fields.RichTextField(_("Content"))
    block_contexts = (ContentBlock,)

    class Meta:
        verbose_name = 'Rich Text'
        verbose_name_plural = 'Rich Text'


class GalleryBlock(ReusableBlock):
    zip_import = models.FileField(verbose_name=_("Zip import"), blank=True,
        upload_to=upload_to("galleries.Gallery.zip_import", "galleries"),
        help_text=_("Upload a zip file containing images, and "
                    "they'll be imported into this gallery."))
    block_contexts = (ContentBlock, AsideBlock)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'

    def save(self, delete_zip_import=True, *args, **kwargs):
        """
        If a zip file is uploaded, extract any images from it and add
        them to the gallery, before removing the zip file.
        """
        super(GalleryBlock, self).save(*args, **kwargs)
        if self.zip_import:
            zip_file = ZipFile(self.zip_import)
            for name in zip_file.namelist():
                data = zip_file.read(name)
                try:
                    from PIL import Image
                    image = Image.open(BytesIO(data))
                    image.load()
                    image = Image.open(BytesIO(data))
                    image.verify()
                except ImportError:
                    pass
                except:
                    continue
                name = os.path.split(name)[1]
                # This is a way of getting around the broken nature of
                # os.path.join on Python 2.x. See also the comment below.
                if isinstance(name, bytes):
                    encoding = charsetdetect(name)['encoding']
                    tempname = name.decode(encoding)
                else:
                    tempname = name

                slug = slugify(self.title)
                path = os.path.join(GALLERIES_UPLOAD_DIR, slug, tempname)
                try:
                    saved_path = default_storage.save(path, ContentFile(data))
                except UnicodeEncodeError:
                    from warnings import warn
                    warn("A file was saved that contains unicode "
                         "characters in its path, but somehow the current "
                         "locale does not support utf-8. You may need to set "
                         "'LC_ALL' to a correct value, eg: 'en_US.UTF-8'.")
                    # The native() call is needed here around str because
                    # os.path.join() in Python 2.x (in posixpath.py)
                    # mixes byte-strings with unicode strings without
                    # explicit conversion, which raises a TypeError as it
                    # would on Python 3.
                    path = os.path.join(GALLERIES_UPLOAD_DIR, slug,
                                        native(str(name, errors="ignore")))
                    saved_path = default_storage.save(path, ContentFile(data))
                self.images.create(file=saved_path)
            if delete_zip_import:
                zip_file.close()
                self.zip_import.delete(save=True)


class GalleryBlockImage(Orderable):
    block = models.ForeignKey(GalleryBlock, related_name="images")
    file = mezzanine_fields.FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("galleries.GalleryImage.file", "galleries"))
    description = models.CharField(_("Description"), max_length=1000,
                                                           blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.
        """
        if not self.id and not self.description:
            name = force_text(self.file)
            name = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            # str.title() doesn't deal with unicode very well.
            # http://bugs.python.org/issue6412
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(GalleryBlockImage, self).save(*args, **kwargs)


class VerticalSpacingBlock(BlockBase):
    height = models.CharField(max_length=10, default='10rem')
    block_contexts = (ContentBlock, AsideBlock)

    class Meta:
        verbose_name = 'Spacer'
        verbose_name_plural = 'Spacers'


class RowSeparatorBlock(BlockBase):
    block_contexts = (ContentBlock,)

    class Meta:
        verbose_name = 'Row Separator'
        verbose_name_plural = 'Row Separators'


class TwitterFeedBlock(ReusableBlock):
    twitter_query = models.ForeignKey(TwitterQuery)
    block_contexts = (AsideBlock,)

    class Meta:
        verbose_name = _("Twitter Feed")
        verbose_name_plural = _("Twitter Feeds")

    @property
    def tweets(self):
        # Re-interest the query each access.
        if not self.twitter_query.interested:
            self.twitter_query.interested = True
            self.twitter_query.save()
        return self.twitter_query.tweets.all()

