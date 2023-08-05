# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.utils.module_loading import autodiscover_modules
from django.contrib.admin import *
from clubhouse.core.options import *

from clubhouse.core.sites import clubhouse
site = clubhouse

def autodiscover():
    autodiscover_modules('admin',register_to=site)
    site.lazy_registration()
