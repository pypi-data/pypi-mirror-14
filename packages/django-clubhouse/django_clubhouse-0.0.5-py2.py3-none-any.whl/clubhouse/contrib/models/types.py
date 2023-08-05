# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from clubhouse.core.models import BlockType

__all__ = ['ContentBlock','AsideBlock']

class ContentBlock(BlockType):
    class Meta:
        verbose_name = 'Content Block'

class AsideBlock(BlockType):
    class Meta:
        verbose_name = 'Aside Block'
