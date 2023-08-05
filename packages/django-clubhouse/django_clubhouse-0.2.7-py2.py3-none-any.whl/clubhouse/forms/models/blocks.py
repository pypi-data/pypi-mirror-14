# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models

from clubhouse.core.models import ReusableBlock
from clubhouse.contrib.models import ContentBlock

__all__ = ['FormBlock']

class FormBlock(ReusableBlock):
    form = models.ForeignKey("clubhouse_forms.Form", on_delete=models.CASCADE)
    block_contexts = (ContentBlock,)

    class Meta:
        verbose_name = 'Form Block'
        verbose_name_plural = 'Form Blocks'

    @property
    def form_object(self):
        from clubhouse.forms import Initialised
        try:
            return Initialised.get("form:%s" % self.pk)
        except KeyError:
            raise ValueError('Form referenced before assignment')

