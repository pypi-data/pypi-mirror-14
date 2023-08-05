# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.admin.filters import SimpleListFilter
from django.utils.translation import ugettext as _, ungettext

__all__ = ['BlockContext']

class BlockContextListFilter(SimpleListFilter):
    title = _('Block Type')
    parameter_name = '_block_type'

    def get_lookup(self, model):
        info = (model._meta.app_label, model._meta.model_name)
        return ('%s.%s' % info, model._meta.verbose_name)

    def lookups(self, request, model_admin):
        return tuple([self.get_lookup(m) for m in model_admin.collect_models()])

    def queryset(self, request, queryset):
        if self.value():
            lookup = self.get_lookup(queryset.model)
            if lookup[0] != self.value():
                return False

        return queryset
