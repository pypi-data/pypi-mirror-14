# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text

from mezzanine.utils.urls import admin_url
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.utils.static import static_lazy as static
from mezzanine.twitter.models import Query as TwitterQuery

from clubhouse import admin
from clubhouse.contrib.models import (
    GalleryBlockImage, GroupingBlock, ContentBlock, AsideBlock, WysiwygBlock,
    GalleryBlock, VerticalSpacingBlock, TwitterFeedBlock, RowSeparatorBlock,
    BlockLibrary
)

__all__ = ['ContentBlockInline','AsideBlockInline','GroupingBlockAdmin',
        'GalleryBlockImageInline','GalleryBlockAdmin']


class ContentBlockInline(admin.BlockInline):
    model = ContentBlock


class AsideBlockInline(admin.BlockInline):
    model = AsideBlock


class GroupingBlockAdmin(admin.BlockAdmin):
    inlines = (ContentBlockInline,)


class GalleryBlockImageInline(TabularDynamicInlineAdmin):
    model = GalleryBlockImage


class GalleryBlockAdmin(admin.BlockAdmin):
    class Media:
        css = {"all": (static("mezzanine/css/admin/gallery.css"),)}

    inlines = (GalleryBlockImageInline,)


class BlockContextsListDisplay(object):
    short_description = _('Contexts')

    def __call__(self,obj):
        b = [force_text(o._meta.verbose_name) for o in obj.block_contexts]
        return ', '.join(b) if b else 'N/a'


class BlockLibraryAdmin(admin.BlockContextAdmin):
    verbose_name = _('Block')
    verbose_name_plural = _('Block Library')

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        # TODO: Insert this somewhere instead of appending to the end.
        ld = super(BlockLibraryAdmin,self).get_list_display(request)
        # TODO: Removed the BlockContextsListDispay, doesn't work with
        # BlockContext.block_models at the minute.. maybe never will due to
        # Inefficiency..
        # return tuple(list(ld) + [BlockContextsListDisplay()])
        return ld


admin.site.register(GalleryBlock, GalleryBlockAdmin)
admin.site.register(GroupingBlock, GroupingBlockAdmin)
admin.site.register([
    WysiwygBlock,
    VerticalSpacingBlock,
    TwitterFeedBlock,
    RowSeparatorBlock,
], admin.BlockAdmin)
admin.site.register(TwitterQuery, admin.ModelAdmin)


admin.site.register(BlockLibrary,BlockLibraryAdmin)

