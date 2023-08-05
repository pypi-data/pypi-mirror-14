# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import inspect
import six

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields import AutoField
from django.apps import apps
from django.utils.text import camel_case_to_spaces
from django.utils.translation import override, string_concat,\
        ugettext as _, ungettext


__all__ = ['BlockBase','BlockType','ReusableBlock']


class ReusableManager(models.Manager):
    def get_queryset(self):
        return super(ReusableManager,self).get_queryset().filter(can_reuse=True)


class BlockBase(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.title)


BLOCK_TYPE_DEFAULT_NAMES = ['verbose_name','verbose_name_plural']

class BlockTypeOptions(object):
    def __init__(self, meta, app_label=None):
        self.verbose_name = None
        self.verbose_name_plural = None
        self.meta = meta
        self.object_name = None

    def contribute_to_class(self, cls, name):
        setattr(cls, name, self)
        self.original_attrs = {}
        self.object_name = cls.__name__
        self.verbose_name = camel_case_to_spaces(self.object_name)

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in BLOCK_TYPE_DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self,attr_name,meta_attrs.pop(attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

            # verbose_name_plural is a special case because it uses a 's'
            # by default.
            if self.verbose_name_plural is None:
                self.verbose_name_plural = string_concat(self.verbose_name, 's')

            # Any leftover attributes must be invalid.
            if meta_attrs != {}:
                raise TypeError("'class Meta' got invalid attribute(s): %s"
                        % ','.join(meta_attrs.keys()))
        else:
            self.verbose_name_plural = string_concat(self.verbose_name, 's')

        del self.meta


class BlockTypeBase(type):
    """
    MetaClass for BlockType
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(BlockTypeBase, cls).__new__

        parents = [b for b in bases if isinstance(b,BlockTypeBase)]
        if not parents:
            return super_new(cls,name,bases,attrs)

        new_class = super_new(cls, name, bases, {'module':attrs.pop('__module__')})
        attr_meta = attrs.pop('Meta', None)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta

        new_class.add_to_class('_meta', BlockTypeOptions(meta))

        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        return new_class

    def add_to_class(cls, name, value):
        if not inspect.isclass(value) and hasattr(value,'contribute_to_class'):
            value.contribute_to_class(cls,name)
        else:
            setattr(cls, name, value)


class BlockType(six.with_metaclass(BlockTypeBase)):
    block_types = ()

    @classmethod
    def get_block_models(cls):
        for m in apps.get_models():
            try:
                if cls in m.block_types:
                    yield m
            except AttributeError:
                pass


class ReusableBlock(BlockBase):
    can_reuse = models.BooleanField(default=False)

    objects = models.Manager()
    reusable = ReusableManager()

    class Meta:
        abstract = True
