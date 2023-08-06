# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from string import punctuation

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from mezzanine.galleries.models import BaseGallery
from mezzanine.core import fields as mezzanine_fields
from mezzanine.core.models import Orderable
from mezzanine.utils.models import upload_to
from mezzanine.twitter.models import Query as TwitterQuery

from clubhouse.core.models import (
    BlockBase, ReusableBlock, AbstractModularComponent
)
from clubhouse.contrib.models.types import ContentBlock, AsideBlock

__all__ = ['GroupingBlock','WysiwygBlock','GalleryBlock',
    'GalleryBlockImage','VerticalSpacingBlock','TwitterFeedBlock',
    'RowSeparatorBlock']


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
    block_contexts = (ContentBlock, AsideBlock, BaseGallery)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Gallery'


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

