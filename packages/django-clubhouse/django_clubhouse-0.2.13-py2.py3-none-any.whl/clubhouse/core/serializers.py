# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import sys, inspect

try:
    from rest_framework import serializers
except ImportError:
    pass
else:
    from django.apps import apps

    def find_for_model(model, app_label=None, serializers_module='serializers'):
        if isinstance(model,basestring):
            model = apps.get_model(*model.split('.'))

        app_label = app_label if app_label else model._meta.app_label
        module_name = '%s.%s' % (app_label,serializers_module)

        try:
            members = sys.modules[module_name]
        except KeyError:
            from importlib import import_module
            import_module(module_name)
            members = sys.modules[module_name]

        for name, obj in inspect.getmembers(members,inspect.isclass):
            try:
                if issubclass(obj, serializers.ModelSerializer)\
                        and obj.Meta.model is model:
                    return obj
            except AttributeError:
                # Probably abstract
                continue

        raise ValueError('Could not find serializer for model: %s' % model)


    class BlockSerializer(serializers.ModelSerializer):
        """
        DEPRECATED: used to include an extended metaclass, but we now use
        the find_for_model in the BlockContextSerializer, so this is deprecated
        Left in for Backward compatability
        """
        pass


    class BlockContextSerializer(serializers.ModelSerializer):
        """
        BlockContaxtSerializer adds the block_object field by default
        """
        block_object = serializers.SerializerMethodField()

        def get_block_object(self, obj):
            try:
                if self.Meta.depth >= 1:
                    serializer = find_for_model(obj.block_object.__class__)
                    return serializer(obj.block_object).data
            except ValueError:
                pass

            return None

