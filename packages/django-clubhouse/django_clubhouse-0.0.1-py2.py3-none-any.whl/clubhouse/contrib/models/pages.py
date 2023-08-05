# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from mezzanine.pages.models import Page

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from clubhouse.utils.enum import Enum, Option


__all__ = ['ModularPage','PageContentBlock','PageAsideBlock','SizeMixin',
           'BlockSizes','PageBlock']


class BlockSizes(Enum):
    SMALL = Option('s',description=_('Small'))
    MEDIUM = Option('m', description=_('Medium'))
    LARGE = Option('l', description=_('Large'))
    SPAN = Option('f', description=_('Span'))


class ModularPage(Page):
    class Meta:
        verbose_name = _('Modular Page')

    @property
    def content(self):
        return self.content_blocks.all()

    @property
    def aside(self):
        return self.aside_blocks.all()


class PageBlockManager(models.Manager):
    def all(self):
        q = models.Q(block_type=None) | models.Q(block_id=None)
        return self.get_queryset().exclude(q)


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


class PageBlock(models.Model):
    block_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    block_id = models.PositiveIntegerField(null=True,blank=True)
    block_object = GenericForeignKey('block_type', 'block_id')
    order = models.PositiveIntegerField(default = 0)
    additional_classes = models.CharField(max_length=255, null=True, blank=True)

    objects = PageBlockManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Remove the block object with the relationship
        """
        try:
            self.block_object.delete()
        except:
            # Could not delete for some reason.. ignore it.
            pass
        return super(PageBlock, self).delete()

    def __unicode__(self):
        return unicode("%s : %s" % (self.block_type, self.block_object))

    @property
    def template(self):
        return self._meta.template_name

    @property
    def classes(self):
        return "%s %s" % (
            self.block_object._meta.model_name,
            self.additional_classes,
        )


class PageContentBlock(PageBlock, SizeMixin):
    page = models.ForeignKey(ModularPage, related_name='content_blocks', on_delete=models.CASCADE)
    class Meta:
        verbose_name = _('Page Content Block')
        verbose_name_plural = _('Page Content Blocks')
        ordering = ('order',)

    @property
    def template(self):
        try:
            return super(PageContentBlock,self).template
        except AttributeError:
            return 'content-blocks/%s.html' % self.block_object._meta.model_name

    @property
    def classes(self):
        return '%s %s' % (super(PageContentBlock,self).classes, self.col_class)


class PageAsideBlock(PageBlock):
    page = models.ForeignKey(ModularPage, related_name='aside_blocks', on_delete=models.CASCADE)
    class Meta:
        verbose_name = _('Page Aside Block')
        verbose_name_plural = _('Page Aside Blocks')
        ordering = ('order',)

    @property
    def template(self):
        try:
            return super(PageAsideBlock,self).template
        except AttributeError:
            return 'aside-blocks/%s.html' % self.block_object._meta.model_name

