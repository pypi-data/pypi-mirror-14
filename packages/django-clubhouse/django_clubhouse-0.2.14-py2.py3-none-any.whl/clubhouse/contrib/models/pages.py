# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from mezzanine.pages.models import Page

from django.db import models
from django.utils.translation import ugettext_lazy as _

from clubhouse.core.models import AbstractModularPage
from clubhouse.contrib.models.types import ContentBlock, AsideBlock

__all__ = ['ModularPage']


class ModularPage(AbstractModularPage):
    class Meta:
        verbose_name = _('Modular Page')

    @property
    def content(self):
        return self.get_blocks_by_context(ContentBlock)

    @property
    def aside(self):
        return self.get_blocks_by_context(AsideBlock)

