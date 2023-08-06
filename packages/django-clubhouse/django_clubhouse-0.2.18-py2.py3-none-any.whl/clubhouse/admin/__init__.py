# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.utils.module_loading import autodiscover_modules
from django.contrib.admin import *
from clubhouse.core.options import *

from mezzanine.pages.admin import PageAdmin as mezz_PageAdmin
from mezzanine.pages.models import Page

from clubhouse.core.sites import clubhouse
site = clubhouse

def autodiscover():
    autodiscover_modules('admin',register_to=site)

    for m in Page.get_content_models():
        try:
            adm = site._registry[m]
        except KeyError:
            continue

        if not isinstance(adm, PageAdmin) and isinstance(adm, mezz_PageAdmin):
            if site.safe_unregister(m):
                site.register(m, PageAdmin)

    site.lazy_registration()

