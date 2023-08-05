# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.apps import AppConfig

from mezzanine.forms import defaults

__all__ = ['ClubHouseFormsConfig','Initialised']


class ClubHouseFormsConfig(AppConfig):
    name = 'clubhouse.forms'
    verbose_name = 'ClubHouse Forms'
    label = 'clubhouse_forms'

default_app_config = 'clubhouse.forms.ClubHouseFormsConfig'


class Initialised(object):
    _forms = {}

    @classmethod
    def register(cls,key,form):
        # if key in cls._forms:
        #     raise KeyError('Overriding form with key %s' % key)
        cls._forms[key] = form

    @classmethod
    def get(cls, key):
        return cls._forms[key]

