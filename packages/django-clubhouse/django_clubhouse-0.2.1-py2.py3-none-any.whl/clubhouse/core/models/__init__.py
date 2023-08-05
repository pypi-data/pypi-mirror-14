# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import inspect
import six

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import AutoField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.utils.text import camel_case_to_spaces
from django.utils.translation import override, string_concat,\
        ugettext as _, ungettext

from mezzanine.pages.models import Page

__all__ = ['BlockBase','BlockContext','ReusableBlock']

def get_page_types():
    qry = None
    for m in Page.get_content_models():
        q = models.Q(app_label=m._meta.app_label, model=m._meta.model_name)
        qry = qry | q if qry else q

    return qry


class ReusableManager(models.Manager):
    def get_queryset(self):
        return super(ReusableManager,self).get_queryset().filter(can_reuse=True)


class BlockBase(models.Model):
    title = models.CharField(max_length=255)

    block_contexts = ()

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.title)


class PageBlockManager(models.Manager):
    def all(self):
        q = models.Q(block_type=None) | models.Q(block_id=None)
        return self.get_queryset().exclude(q)


class BlockContext(models.Model):
    block_type = models.ForeignKey(ContentType, null=True, blank=True,
            on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_block')
    block_id = models.PositiveIntegerField(null=True,blank=True)
    block_object = GenericForeignKey('block_type', 'block_id')
    parent_type = models.ForeignKey(ContentType, null=True, blank=True,
            on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_parent')
    parent_id = models.PositiveIntegerField(null=True,blank=True)
    parent_object = GenericForeignKey('parent_type', 'parent_id')

    order = models.PositiveIntegerField(default = 0)
    additional_classes = models.CharField(max_length=255, null=True, blank=True)

    objects = PageBlockManager()

    class Meta:
        abstract = True

    @classmethod
    def get_block_models(cls):
        """
        Default method of getting the block models for this type.
        Can override this method with other methods, but must return an
        iterable of model classes.
        """
        for model in apps.get_models():
            try:
                if issubclass(model, BlockBase) and cls in model.block_contexts:
                    yield model
            except AttributeError:
                pass

    def delete(self, *args, **kwargs):
        """
        Remove the block object with the relationship
        """
        try:
            self.block_object.delete()
        except:
            # Could not delete for some reason.. ignore it.
            pass
        return super(BlockContext, self).delete(*args, **kwargs)

    def __unicode__(self):
        return unicode("%s : %s" % (self.block_type, self.block_object))

    @property
    def classes(self):
        return "%s %s" % (
            self.block_object._meta.model_name,
            self.additional_classes,
        )


class ReusableBlock(BlockBase):
    can_reuse = models.BooleanField(default=False)

    objects = models.Manager()
    reusable = ReusableManager()

    class Meta:
        abstract = True
