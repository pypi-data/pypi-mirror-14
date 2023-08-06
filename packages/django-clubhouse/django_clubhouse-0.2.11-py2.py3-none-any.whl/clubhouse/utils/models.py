# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet


class SubclassingQuerySet(QuerySet):
    """
    Ensures the correct model is being returned from any parent abstraction.
    """
    def __getitem__(self,k):
        res = super(SubclassingQuerySet,self).__getitem__(k)
        if isinstance(res, models.Model):
            return res.as_leaf_class()
        else:
            return res

    def __iter__(self):
        for item in super(SubclassingQuerySet, self).__iter__():
            yield item.as_leaf_class()


class SubclassingManager(models.Manager):
    def get_query_set(self):
        return SubclassingQuerySet(self.model)


class SubclassableModel(models.Model):
    """
    Extend this model and the default manager will always return the appropriate
    subclass model when querying from the parent.
    """
    content_type = models.ForeignKey(ContentType, editable=False,null=True)

    default_manager = SubclassingManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(SubclassableModel, self).save(*args,**kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if model == self.__class__:
            return self
        return model.objects.get(pk=self.pk)
