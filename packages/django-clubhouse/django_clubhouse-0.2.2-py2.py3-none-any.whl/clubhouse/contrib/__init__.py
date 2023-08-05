# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.apps import AppConfig

__all__ = ['ClubHouseContribConfig']

class ClubHouseContribConfig(AppConfig):
    name = 'clubhouse.contrib'
    verbose_name = 'ClubHouse Contrib'
    label = 'clubhouse_contrib'

default_app_config = 'clubhouse.contrib.ClubHouseContribConfig'

