# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf import settings

from rest_framework import serializers

from clubhouse.core.options import serializer_registry as registry
from clubhouse.core.serializers import (
    BlockSerializer, BlockContextSerializer
)
from clubhouse.contrib.models.blocks import *
from clubhouse.contrib.models.types import *
from clubhouse.contrib.models.pages import *


#######################################
###### BLOCK CONTEXT SERIALIZERS ######
#######################################

class ContentBlockSerializer(BlockContextSerializer):
    class Meta:
        model = ContentBlock
        depth = 1


class AsideBlockSerializer(BlockContextSerializer):
    class Meta:
        model = AsideBlock
        depth = 1


class GroupingBlockSerializer(BlockSerializer):
    content_blocks = serializers.SerializerMethodField()

    class Meta:
        model = GroupingBlock

    def get_content_blocks(self, obj):
        return [ContentBlockSerializer(c).data for c in obj.content]


#############################
##### BLOCK SERIALIZERS #####
#############################

class WysiwygBlockSerializer(BlockSerializer):
    class Meta:
        model = WysiwygBlock


class GalleryBlockImageSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryBlockImage
        exclude = ('file','block')

    def get_img_url(self, obj):
        return '%s%s' % (settings.MEDIA_URL, obj.file)


class GalleryBlockSerializer(BlockSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = GalleryBlock

    def get_images(self, obj):
        return [GalleryBlockImageSerializer(img).data\
                for img in obj.images.all()]


class VerticalSpacingBlockSerializer(BlockSerializer):
    class Meta:
        model = VerticalSpacingBlock


class RowSeparatorBlockSerializer(BlockSerializer):
    class Meta:
        model = RowSeparatorBlock


class TwitterFeedBlockSerializer(BlockSerializer):
    class Meta:
        model = TwitterFeedBlock


############################
##### PAGE SERIALIZERS #####
############################

class ModularPageSerializer(serializers.ModelSerializer):
    content_blocks = serializers.SerializerMethodField()
    aside_blocks = serializers.SerializerMethodField()

    class Meta:
        model = ModularPage

    def get_content_blocks(self, obj):
        # TODO: change this to hyperlinked?
        return [ContentBlockSerializer(c).data for c in obj.content]

    def get_aside_blocks(self, obj):
        # TODO: change this to hyperlinked?
        return [AsideBlockSerializer(c).data for c in obj.aside]


registry.add(ContentBlockSerializer)
registry.add(AsideBlockSerializer)
registry.add(GroupingBlockSerializer)
registry.add(WysiwygBlockSerializer)
registry.add(GalleryBlockSerializer)
registry.add(GalleryBlockImageSerializer)
registry.add(VerticalSpacingBlockSerializer)
registry.add(RowSeparatorBlockSerializer)
registry.add(TwitterFeedBlockSerializer)
registry.add(ModularPageSerializer)

