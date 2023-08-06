# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import six

try:
    from rest_framework import serializers
except ImportError:
    pass
else:
    from django.utils.module_loading import autodiscover_modules
    from clubhouse.core.models import BlockBase

    class SerializerMetaclass(serializers.SerializerMetaclass):
        """
        Adds _serializers to models
        Adds default_serializer if not already defined
        """
        def __new__(cls, name, bases, attrs):
            new = super(SerializerMetaclass,cls).__new__(cls,name,bases,attrs)
            try:
                model = new.Meta.model
            except AttributeError:
                # Serializer doesn't have model class.. probably abstract
                pass
            else:
                new.contribute_to_class(model, '_serializers')

            return new

        def contribute_to_class(self, cls, name):
            # Only apply this to blocks.. as thats all we care about
            if not issubclass(cls, BlockBase):
                return

            if not hasattr(cls, 'default_serializer'):
                # set the default serializer if not already set
                cls.default_serializer = self

            try:
                if self.Meta.replace_default:
                    cls.default_serializer = self
            except AttributeError:
                pass

            # Set the attribute by appending self to list of serializers
            setattr(cls, name, getattr(cls, name, []).append(self))


    @six.add_metaclass(SerializerMetaclass)
    class BlockSerializer(serializers.ModelSerializer):
        pass


    class BlockContextSerializer(serializers.ModelSerializer):
        """
        BlockContaxtSerializer adds the block_object field by default
        """
        block_object = serializers.SerializerMethodField()

        def get_block_object(self, obj):
            try:
                if self.Meta.depth >= 1:
                    return obj.block_object\
                            .default_serializer(obj.block_object).data
            except AttributeError:
                pass

            return None

    # Auto discover serializers modules in order to register the
    # default_serializer
    autodiscover_modules('serializers')
