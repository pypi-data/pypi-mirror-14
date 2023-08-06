# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import inspect
import six

from django.db import models
from django.conf import settings
from django.db.models.base import ModelBase
from django.db.models.fields import AutoField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.utils.text import camel_case_to_spaces
from django.utils.translation import override, string_concat,\
        ugettext as _, ungettext
from django.utils import timezone
from django.conf import settings

from mezzanine.pages.models import Page

from clubhouse.utils.models import ensure_model

__all__ = ['BlockBase','BlockContext','ReusableBlock','AbstractModularPage']

try:
    User = settings.AUTH_USER_MODEL
except AttributeError:
    from django.contrib.auth.models import User


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

    date_created = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey(User, null=True, blank=True, editable=False,
            related_name='%(app_label)s_%(class)s_blocks_created')
    last_updated = models.DateTimeField(auto_now=True)
    user_updated = models.ForeignKey(User, null=True, blank=True, editable=False,
            related_name='%(app_label)s_%(class)s_blocks_updated')

    block_contexts = ()

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.title)

    def get_template(self):
        return 'blocks/%s.html' % self._meta.model_name


class PageBlockManager(models.Manager):
    def all(self):
        q = models.Q(block_type=None) | models.Q(block_id=None)
        return self.get_queryset().exclude(q)


class BlockContext(models.Model):
    block_type = models.ForeignKey(ContentType, null=True, blank=True,
            on_delete=models.CASCADE,
            related_name='%(app_label)s_%(class)s_block')
    block_id = models.PositiveIntegerField(null=True,blank=True)
    block_object = GenericForeignKey('block_type', 'block_id')
    parent_type = models.ForeignKey(ContentType, null=True, blank=True,
            on_delete=models.SET_NULL, related_name='%(app_label)s_%(class)s_parent')
    parent_id = models.PositiveIntegerField(null=True,blank=True)
    parent_object = GenericForeignKey('parent_type', 'parent_id')

    order = models.PositiveIntegerField(default = 0)
    additional_classes = models.CharField(max_length=255, null=True, blank=True,
            help_text='Space separated list of additional css classes')

    objects = PageBlockManager()

    block_models = tuple()

    class Meta:
        abstract = True
        ordering = ('order',)

    @classmethod
    def get_block_models(cls):
        """
        Default method of getting the block models for this type.
        Can override this method with other methods, but must return an
        iterable of model classes.
        """
        yielded = []
        for block in cls.block_models:
            try:
                block = ensure_model(block)
                info = "%s.%s" % (block._meta.app_label, block._meta.model_name)
                if info in yielded:
                    continue
                yield block
                yielded.append(info)
            except ValueError:
                if settings.DEBUG:
                    # Help figure out why blocks arn't displayed
                    raise
                pass

        for model in apps.get_models():
            try:
                contexts = []
                for c in model.block_contexts:
                    try:
                        contexts.append(ensure_model(c))
                    except ValueError:
                        if settings.DEBUG:
                            # Help figure out why blocks arn't displayed
                            raise
                        pass
                if issubclass(model, BlockBase) and cls in contexts:
                    info = "%s.%s" % (model._meta.app_label,model._meta\
                            .model_name)
                    if info in yielded:
                        continue
                    yield model
                    yielded.append(info)
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

    @classmethod
    def get_template(cls):
        return '%s.html' % cls._meta.model_name


class ReusableBlock(BlockBase):
    can_reuse = models.BooleanField(default=False)

    objects = models.Manager()
    reusable = ReusableManager()

    class Meta:
        abstract = True


class AbstractModularComponent(models.Model):
    class Meta:
        abstract = True

    def get_blocks_by_context(self, context):
        ct = ContentType.objects.get_for_model(self.__class__)
        return context.objects.filter(parent_type=ct, parent_id=self.pk)\
                .order_by('order')


class AbstractModularPage(Page, AbstractModularComponent):
    class Meta:
        abstract = True

