# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models
from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from clubhouse.core.models import BlockContext, BlockBase
from clubhouse.utils.enum import Enum, Option

__all__ = ['ContentBlock','AsideBlock','SizeMixin','BlockLibrary']


class BlockLibrary(BlockContext):
    """
    Abstract model to be used as an All block admin page, i.e. Block Library
    You can extend this and use as a BlockContext if you want all blocks in
    a certain place.
    """
    class Meta:
        abstract = True
        verbose_name = _('Block Library')
        verbose_name_plural = _('Block Library')

    @classmethod
    def get_block_models(cls):
        for model in apps.get_models():
            if issubclass(model, BlockBase):
                yield model


class BlockSizes(Enum):
    SMALL = Option('s',description=_('Small'))
    MEDIUM = Option('m', description=_('Medium'))
    LARGE = Option('l', description=_('Large'))
    SPAN = Option('f', description=_('Span'))


class SizeMixin(models.Model):
    size = models.CharField(max_length=1, default=BlockSizes.MEDIUM, null=True, blank=True, choices=BlockSizes.get_choices())

    class Meta:
        abstract = True

    @property
    def col_class(self):
        if self.size == BlockSizes.SMALL:
            return 'col-md-3'
        elif self.size == BlockSizes.MEDIUM:
            return 'col-md-6'
        elif self.size == BlockSizes.LARGE:
            return 'col-md-9'
        elif self.size == BlockSizes.SPAN:
            return 'col-md-12'


class ContentBlock(BlockContext, SizeMixin):
    class Meta:
        verbose_name = _('Content Block')
        verbose_name_plural = _('Content Blocks')

    @property
    def template(self):
        try:
            return super(ContentBlock,self).template
        except AttributeError:
            return 'content-blocks/%s.html' % self.block_object._meta.model_name

    @property
    def classes(self):
        return '%s %s' % (super(PageContentBlock,self).classes, self.col_class)


class AsideBlock(BlockContext):
    class Meta:
        verbose_name = _('Aside Block')
        verbose_name_plural = _('Aside Blocks')
        ordering = ('order',)

    @property
    def template(self):
        try:
            return super(AsideBlock,self).template
        except AttributeError:
            return 'aside-blocks/%s.html' % self.block_object._meta.model_name

