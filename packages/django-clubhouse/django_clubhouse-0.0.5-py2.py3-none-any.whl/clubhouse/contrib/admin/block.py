# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import re

from django.db import models

from mezzanine.utils.urls import admin_url
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.utils.static import static_lazy as static
from mezzanine.twitter.models import Query as TwitterQuery

from clubhouse import admin
from clubhouse.admin import BlockInline
from clubhouse.contrib.models import GalleryBlockImage,\
        GroupContentBlock, ContentBlock, AsideBlock, WysiwygBlock, GalleryBlock,\
        GroupingBlock, VerticalSpacingBlock, TwitterFeedBlock, RowSeparatorBlock


class GroupingContentBlockInline(BlockInline):
    model = GroupContentBlock
    block_type = ContentBlock


class GroupingBlockAdmin(admin.BlockAdmin):
    inlines = (GroupingContentBlockInline,)


class GalleryBlockImageInline(TabularDynamicInlineAdmin):
    model = GalleryBlockImage


class GalleryBlockAdmin(admin.BlockAdmin):
    class Media:
        css = {"all": (static("mezzanine/css/admin/gallery.css"),)}

    inlines = (GalleryBlockImageInline,)


admin.site.register(GalleryBlock, GalleryBlockAdmin)
admin.site.register(GroupingBlock, GroupingBlockAdmin)
admin.site.register([
    WysiwygBlock,
    VerticalSpacingBlock,
    TwitterFeedBlock,
    RowSeparatorBlock,
], admin.BlockAdmin)
admin.site.register(TwitterQuery, admin.ModelAdmin)


admin.site.register_block_type([
    ContentBlock,
    AsideBlock
])

