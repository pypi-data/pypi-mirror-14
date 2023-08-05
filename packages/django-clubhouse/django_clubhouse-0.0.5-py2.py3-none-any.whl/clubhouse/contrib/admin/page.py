# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from clubhouse import admin
from clubhouse.contrib.models import ModularPage,PageContentBlock,\
        PageAsideBlock,ContentBlock,AsideBlock
from clubhouse.admin import BlockInline
from clubhouse.core.options import PageAdmin

__all__ = ['ModularPageAdmin','PageContentBlockInline','PageAsideBlockInline']


class PageContentBlockInline(BlockInline):
    model = PageContentBlock
    block_type = ContentBlock


class PageAsideBlockInline(BlockInline):
    model = PageAsideBlock
    block_type = AsideBlock


class ModularPageAdmin(PageAdmin):
    inlines = (
        PageAsideBlockInline,
        PageContentBlockInline
    )


admin.site.register(ModularPage,ModularPageAdmin)
