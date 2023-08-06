# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import copy
from importlib import import_module

from django.apps import AppConfig

from django.db.models import options

__all__ = ['ClubHouseCoreConfig','site']

class ClubHouseCoreConfig(AppConfig):
    name = 'clubhouse.core'
    verbose_name = 'ClubHouse Core'
    label = 'clubhouse_core'

default_app_config = 'clubhouse.core.ClubHouseCoreConfig'

from clubhouse.core.sites import clubhouse
site = clubhouse
