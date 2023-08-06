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

    from clubhouse.utils.models import ensure_model

    def find_for_model(model, app_label=None, serializers_module='serializers'):
        """
        This is extends the serializer_registry.find_for_model by searching
        installed the app provided by either the app_label arg or the
        model._meta.app_label property, and the serializers_module arg
        it will loop through any classes found in this module and check for a
        Meta.model property matching the provided model and return if found.

        i.e. it will return the first modelserializer it finds matching provided
        model in the app.module provided, if non found raises ValueError
        """
        from clubhouse.core.options import serializer_registry, NotRegistered
        try:
            return serializer_registry.find_for_model(model)
        except NotRegistered:
            pass

        # In the event the serializer is not registered, return the first
        # serializer found in the app provided by app_label.serializer_module
        model = ensure_model(model)
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
            from clubhouse.core.options import serializer_registry as registry
            try:
                if self.Meta.depth >= 1:
                    model_class = obj.block_object.__class__
                    serializer = find_for_model(model_class)
                    return serializer(obj.block_object).data
            except ValueError:
                pass

            return None



