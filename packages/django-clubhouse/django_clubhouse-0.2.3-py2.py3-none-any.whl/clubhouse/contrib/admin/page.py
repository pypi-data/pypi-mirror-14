# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from clubhouse import admin
from clubhouse.contrib.models import ModularPage,ContentBlock,AsideBlock
from clubhouse.contrib.admin.block import ContentBlockInline,AsideBlockInline
from clubhouse.admin import BlockInline
from clubhouse.core.options import PageAdmin

__all__ = ['ModularPageAdmin']


class ModularPageAdmin(PageAdmin):
    inlines = (
        AsideBlockInline,
        ContentBlockInline
    )


admin.site.register(ModularPage,ModularPageAdmin)

