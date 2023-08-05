# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from clubhouse.core.models import BlockType
from clubhouse.utils.enum import Enum, Option

__all__ = ['ContentBlock','AsideBlock','SizeMixin']


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


class ContentBlock(BlockType, SizeMixin):
    class Meta:
        verbose_name = _('Page Content Block')
        verbose_name_plural = _('Page Content Blocks')
        ordering = ('order',)

    @property
    def template(self):
        try:
            return super(ContentBlock,self).template
        except AttributeError:
            return 'content-blocks/%s.html' % self.block_object._meta.model_name

    @property
    def classes(self):
        return '%s %s' % (super(PageContentBlock,self).classes, self.col_class)


class AsideBlock(BlockType):
    class Meta:
        verbose_name = _('Page Aside Block')
        verbose_name_plural = _('Page Aside Blocks')
        ordering = ('order',)

    @property
    def template(self):
        try:
            return super(AsideBlock,self).template
        except AttributeError:
            return 'aside-blocks/%s.html' % self.block_object._meta.model_name

