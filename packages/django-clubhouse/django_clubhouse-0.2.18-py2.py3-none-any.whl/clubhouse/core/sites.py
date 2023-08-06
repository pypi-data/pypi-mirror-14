# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered, AdminSite
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.db.models.base import ModelBase
from django.contrib.admin.options import ModelAdmin

from mezzanine.boot.lazy_admin import LazyAdminSite
from mezzanine.conf import settings as mezzanine_settings

from clubhouse.core.views.related import AutocompleteLookup,\
        RelatedLookup, M2MLookup
from clubhouse.core.models import BlockBase, BlockContext
from clubhouse.core.settings import (
    BLOCK_MENU_SECTION, BLOCK_MENU_INDEX
)

__all__ = ['clubhouse']


class ClubHouse(LazyAdminSite):
    def __init__(self, *args, **kwargs):
        self._block_type_admins = {}
        super(ClubHouse,self).__init__(*args,**kwargs)

    def register(self, model_or_iterable, admin_class=None, **options):
        if isinstance(model_or_iterable,ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if issubclass(model, BlockContext):
                self.register_block_type(model, admin_class)
                continue
            if not admin_class and issubclass(model, BlockBase):
                from clubhouse.core.options import BlockAdmin
                admin_class = BlockAdmin
            super(ClubHouse,self).register(model, admin_class, **options)

    def unregister(self, model_or_iterable, *args, **kwargs):
        if isinstance(model_or_iterable, ModelBase):
            if issubclass(model_or_iterable, BlockContext):
                return self.unregister_block_type(model_or_iterable)
            super(ClubHouse,self).unregister(model_or_iterable, *args, **kwargs)
        else:
            for m in model_or_iterable:
                self.unregister(m,*args,**kwargs)

    def safe_unregister(self, *args, **kwargs):
        """
        Checks the deferred unregister for an existing unregister and doesn't
        add another one for this model

        returns False if this unregister call was skipped
        returns True if this unregister call was added

        This is mostly for re-registering Page models to the
        Clubhouse.admin.PageAdmin class..

        """
        # TODO: Possibly a smarter unregister / register check
        # this method assumes that if the admin has been unregistered
        # and needs to be re-registered you will use the clubhouse.PageAdmin
        # class.
        for name, deferred_args, deferred_kwargs in self._deferred:
            if name == "unregister" and deferred_args[0] == args[0]:
                return False
        else:
            self.unregister(*args, **kwargs)
            return True

    def register_block_type(self,type_or_iterable,admin_class=None,**options):
        """
        BlockAdmin classes can register multiple block types.
        """
        if not admin_class:
            from clubhouse.core.options import BlockContextAdmin
            admin_class = BlockContextAdmin
        if not isinstance(type_or_iterable,(list, tuple)):
            type_or_iterable = [type_or_iterable]
        for t in type_or_iterable:
            if t in self._block_type_admins:
                raise AlreadyRegistered('The block type %s is already '
                        'registered' % t)
            self._block_type_admins[t] = admin_class(block_type=t,admin_site=self)

    def unregister_block_type(self, type_or_iterable):
        if issubclass(type_or_iterable,BlockContext):
            type_or_iterable = [type_or_iterable]
        for t in type_or_iterable:
            if not t in self._block_type_admins:
                raise NotRegistered('Block admin %s is not registered' % t)
            del self._block_type_admins[t]

    def each_context(self,request):
        for typ,admin_inst in self._block_type_admins.items():
            if not admin_inst.has_change_permission(request):
                continue

            # Inject the block change list into the Admin menu
            insert = lambda n, k, i: getattr(mezzanine_settings,n,[]).insert(i, k)\
                    if k not in getattr(mezzanine_settings,n,[]) else None

            tuple_list_settings = ["ADMIN_MENU_ORDER"]
            for s in tuple_list_settings[:]:
                if not isinstance(getattr(mezzanine_settings,s,[]),list):
                    setattr(mezzanine_settings,s,list(getattr(mezzanine_settings,s)))
                else:
                    tuple_list_settings.remove(s)

            info = (admin_inst._meta.app_label, admin_inst.block_type_name)
            changelist_name = '%s_%s_changelist' % info
            block_menu_item = (
                admin_inst.verbose_name_plural, 'admin:%s' % changelist_name
            )

            for i, (item_name, item) in enumerate(mezzanine_settings.ADMIN_MENU_ORDER):
                if item_name == BLOCK_MENU_SECTION:
                    buff = item
                    item = list(item) if not isinstance(item,list) else item

                    item.append(block_menu_item)

                    if isinstance(buff,tuple):
                        item = tuple(item)
                    mezzanine_settings.ADMIN_MENU_ORDER[i] = (item_name,item)
                    break
            else:
                insert('ADMIN_MENU_ORDER', (BLOCK_MENU_SECTION,
                    (block_menu_item,)),BLOCK_MENU_INDEX)

            for s in tuple_list_settings:
                setattr(settings,s,tuple(getattr(settings,s)))

        return super(ClubHouse,self).each_context(request)

    def check_dependencies(self):
        """
        Check that all things needed to run the admin have been correctly installed.
        The default implementation checks that admin and contenttypes apps are
        installed, as well as the auth context processor.

        Copyed and modified from django base site.
        """
        if not apps.is_installed('clubhouse.core'):
            raise ImproperlyConfigured(
                "Put 'clubhouse.core' in your INSTALLED_APPS "
                "setting in order to use the admin application.")
        if not apps.is_installed('django.contrib.contenttypes'):
            raise ImproperlyConfigured(
                "Put 'django.contrib.contenttypes' in your INSTALLED_APPS "
                "setting in order to use the admin application.")
        try:
            default_template_engine = Engine.get_default()
        except Exception:
            # Skip this non-critical check:
            # 1. if the user has a non-trivial TEMPLATES setting and Django
            #    can't find a default template engine
            # 2. if anything goes wrong while loading template engines, in
            #    order to avoid raising an exception from a confusing location
            # Catching ImproperlyConfigured suffices for 1. but 2. requires
            # catching all exceptions.
            pass
        else:
            if ('django.contrib.auth.context_processors.auth'
                    not in default_template_engine.context_processors):
                raise ImproperlyConfigured(
                    "Enable 'django.contrib.auth.context_processors.auth' "
                    "in your TEMPLATES setting in order to use the admin "
                    "application.")

    def get_urls(self):
        urls = [
            # FOREIGNKEY & GENERIC LOOKUP
            url(r'^lookup/related/$', RelatedLookup.as_view(), name="grp_related_lookup"),
            url(r'^lookup/m2m/$', M2MLookup.as_view(), name="grp_m2m_lookup"),
            url(r'^lookup/autocomplete/$', AutocompleteLookup.as_view(), name="grp_autocomplete_lookup"),
        ] + super(ClubHouse,self).get_urls()

        for typ, inst in self._block_type_admins.items():
            urls += inst.get_urls()

        return urls

clubhouse = ClubHouse()

import django.contrib.admin
django.contrib.admin.site = clubhouse
