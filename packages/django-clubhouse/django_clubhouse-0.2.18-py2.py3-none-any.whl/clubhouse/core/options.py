# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import inspect
import six
import operator
from collections import OrderedDict
from functools import update_wrapper
import re

from django import forms
from django.db import models
from django.conf import settings
from django.apps import apps
from django.utils.text import camel_case_to_spaces
from django.utils.translation import override, string_concat,\
        ugettext as _, ungettext
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered
from django.core.urlresolvers import NoReverseMatch
from django.contrib.admin.options import BaseModelAdmin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.core.paginator import Paginator
from django.contrib.admin.sites import AlreadyRegistered, NotRegistered
from django.contrib.admin import helpers
from django.conf.urls import url,include
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.http import Http404, HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.utils.encoding import force_text
from django.utils.module_loading import autodiscover_modules
from django.contrib.admin.templatetags.admin_static import static
from django.db.models.base import ModelBase
from django.contrib.admin.options import (
    IS_POPUP_VAR, TO_FIELD_VAR, IncorrectLookupParameters,
)
from django.contrib.admin.utils import lookup_needs_distinct
from django.utils.http import urlencode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericStackedInline

from mezzanine.utils.urls import admin_url
from mezzanine.pages.admin import PageAdmin as mezzanine_PageAdmin

from clubhouse.core.models import BlockContext, ReusableBlock, BlockBase
from clubhouse.core.filters import BlockContextListFilter
from clubhouse.core import widgets
from clubhouse.utils.models import ensure_model

from image_cropping import ImageCroppingMixin
from image_cropping import widgets as img_widgets

__all__ = ['BlockContextAdmin','BlockContextAdminBase','BlockAdmin',
        'BlockInline','PageAdmin','FileBrowseImageCroppingMixin',
        'serializer_registry','autodiscover_serializers','NotRegistered',
        'AlreadyRegistered']

DEFAULT_NAMES = ('verbose_name','verbose_name_plural','permissions','ordering',
        'default_permissions', 'base_block')


class BlockTypeListDisplay(object):
    short_description = _('Type')

    def __call__(self,obj):
        return obj._meta.verbose_name


class BlockContextAdminOptions(object):
    def __init__(self, meta, app_label=None):
        self.ordering = []
        self.default_permissions = ('add', 'change', 'delete')
        self.permissions = []
        self.app_label = app_label
        self.meta = meta
        self.object_name = None
        # The base model for the block type.  ensures all inherited
        # blocks have the correct fields
        self.base_block = ReusableBlock
        self.app_config = None

    def _prepare(self,admin):
        # Here for future usage
        pass

    def contribute_to_class(self, cls, name):
        setattr(cls, name, self)
        self.original_attrs = {}
        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__:
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in DEFAULT_NAMES:
                if attr_name in meta_attrs:
                    setattr(self,attr_name,meta_attrs.pop(attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self.meta, attr_name))
                    self.original_attrs[attr_name] = getattr(self, attr_name)

        del self.meta

        self.object_name = self.base_block.__name__

        if self.app_label is None:
            module = self.base_block.__module__
            self.app_config = apps.get_containing_app_config(module)
            self.app_label = self.app_config.label

    @property
    def label(self):
        return '%s.%s' % (self.app_label, self.object_name)


class BlockContextAdminBase(forms.MediaDefiningClass):
    """
    MetaClass for BlockAdmin
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(BlockContextAdminBase, cls).__new__

        buff_attrs = {'module':attrs.pop('__module__')}
        try:
            buff_attrs.update({'media': attrs.pop('media')})
        except KeyError:
            pass
        new_class = super_new(cls, name, bases, buff_attrs)
        attr_meta = attrs.pop('Meta', None)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta

        new_class.add_to_class('_meta', BlockContextAdminOptions(meta))

        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)

        new_class._prepare()
        return new_class

    def _prepare(cls):
        opts = cls._meta
        opts._prepare(cls)

    def add_to_class(cls, name, value):
        if not inspect.isclass(value) and hasattr(value,'contribute_to_class'):
            value.contribute_to_class(cls,name)
        else:
            setattr(cls, name, value)


class BlockContextAdmin(six.with_metaclass(BlockContextAdminBase,BaseModelAdmin)):
    "Encapsulates all admin options and functionality for a given block type."

    list_display = ('title','user_created','date_created','last_updated')
    list_display_links = ()
    list_filter = ('user_created','date_created')
    list_select_related = False
    list_per_page = 100
    list_max_show_all = 200
    list_editable = ()
    search_fields = ('title',)
    date_hierarchy = None
    # save_as = False
    # save_on_top = False
    paginator = Paginator
    preserve_filters = True
    # inlines = []

    # Custom templates (designed to be over-ridden in subclasses)
    # add_form_template = None
    # change_form_template = None
    change_list_template = None
    # delete_confirmation_template = None
    delete_selected_confirmation_template = None
    # TODO: Object history.
    # object_history_template = None

    # Actions
    actions = []
    action_form = helpers.ActionForm
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True

    verbose_name = None
    verbose_name_plural = None

    # validation
    # TODO: Validation per model
    # Old, deprecated style:
    # default_validator_class = validation.ModelAdminValidator
    # New style:
    # checks_class = ModelAdminChecks

    class Meta:
        base_block = ReusableBlock

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        js = [
            'core.js',
            'admin/RelatedObjectLookups.js',
            'jquery%s.js' % extra,
            'jquery.init.js'
        ]
        css = [
            'block_admin.css'
        ]
        # if self.actions is not None:
        #     js.append('actions%s.js' % extra)
        # if self.prepopulated_fields:
        #     js.extend(['urlify.js', 'prepopulate%s.js' % extra])

        return forms.Media(
            js=[static('admin/js/%s' % url) for url in js],
            css={'all': [static('admin/css/%s' % url) for url in css]}
        )

    def __init__(self, block_type, admin_site):
        if not issubclass(block_type, BlockContext):
            raise ImproperlyConfigured('Block type %s does not extend '
                    'clubhouse_core.BlockContext' % block_type.__class__\
                            .__name__)

        if not issubclass(self._meta.base_block, ReusableBlock):
            raise ImproperlyConfigured('Base block %s must extends clubhouse_core'
                    '.ReusableBlock' % self._meta.base_block.__class__.__name__)

        class ProxyPK(object):
            attname = 'id'

        self.model = self._meta.base_block
        if getattr(self.model._meta, 'pk', None) is None:
            self.model._meta.pk = ProxyPK()

        self.block_type = block_type
        self.block_type_name = block_type.__name__.lower()

        if self.verbose_name is None:
            self.verbose_name = block_type._meta.verbose_name
        if self.verbose_name_plural is None:
            self.verbose_name_plural = block_type._meta.verbose_name_plural

        self.admin_site = admin_site
        super(BlockContextAdmin,self).__init__()

    def collect_models(self):
        """
        Generator
        Gets a list of models that have been registered to the admin site, and
        extends the base_block attribute of _meta
        """
        for m in self.block_type.get_block_models():
            if m in self.admin_site._registry and issubclass(m, self.model):
                yield m

    def get_urls(self):
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = (self._meta.app_label, self.block_type_name)
        changelist_name = '%s_%s_changelist' % info

        # Admin-site-wide views.
        urlpatterns = [
            url(r'^%s/%s/$' % info,wrap(self.changelist_view),name=changelist_name)
        ]
        return urlpatterns

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        # TODO: Insert this somewhere instead of appending to the end.
        return tuple(list(self.list_display) + [BlockTypeListDisplay()])

    def get_list_display_links(self,request,list_display):
        """
        Return a sequence containing the fields to be displayed as links
        on the changelist. The list_display parameter is the list of fields
        returned by get_list_display().
        """
        if self.list_display_links or self.list_display_links is None or not list_display:
            return self.list_display_links
        else:
            # Use only the first item in list_display as link
            return list(list_display)[:1]

    def get_list_filter(self,request):
        """
        Returns a sequence containing the fields to be displayed as filters in
        the right sidebar of the changelist page.
        """
        return tuple([BlockContextListFilter] + list(self.list_filter))

    def get_search_fields(self, request):
        """
        Returns a sequence containing the fields to be searched whenever
        somebody submits a search query.
        """
        return self.search_fields

    def get_actions(self, request):
        """
        Return a dictionary mapping the names of all actions for this
        ModelAdmin to a tuple of (callable, name, description) for each action.
        """
        # If self.actions is explicitly set to None that means that we don't
        # want *any* actions enabled on this page.
        if self.actions is None or IS_POPUP_VAR in request.GET:
            return OrderedDict()

        actions = []

        # Gather actions from the admin site first
        for (name, func) in self.admin_site.actions:
            description = getattr(func, 'short_description', name.replace('_', ' '))
            actions.append((func, name, description))

        # get_action might have returned None, so filter any of those out.
        actions = filter(None, actions)

        # Convert the actions into an OrderedDict keyed by name.
        actions = OrderedDict(
            (name, (func, name, desc))
            for func, name, desc in actions
        )

        return actions

    def get_search_fields(self, request):
        """
        Returns a sequence containing the fields to be searched whenever
        somebody submits a search query.
        """
        return self.search_fields

    def get_search_results(self, request, queryset, search_term):
        """
        Returns a tuple containing a queryset to implement the search,
        and a boolean indicating if the results may contain duplicates.
        """
        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        use_distinct = False
        search_fields = self.get_search_fields(request)
        if search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            if not use_distinct:
                for search_spec in orm_lookups:
                    if lookup_needs_distinct(queryset.model._meta, search_spec):
                        use_distinct = True
                        break

        return queryset, use_distinct

    def get_paginator(self, request, queryset, per_page, orphans=0, allow_empty_first_page=True):
        return self.paginator(queryset, per_page, orphans, allow_empty_first_page)

    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        return {m: m.reusable.get_queryset() for m in self.collect_models()}

    def has_add_permission(self,request):
        for model in self.collect_models():
            try:
                admin = self.admin_site._registry[model]
            except KeyError:
                continue
            else:
                if admin.has_add_permission(request):
                    return True
        return False

    def has_change_permission(self,request,obj=None):
        for model in self.collect_models():
            try:
                admin = self.admin_site._registry[model]
            except KeyError:
                continue
            else:
                if admin.has_change_permission(request,obj):
                    return True
        return False

    def get_changelist(self, request, **kwargs):
        """
        Returns the ChangeList class for use on the changelist page.
        """
        from clubhouse.core.views.admin import BlockContextChangeList
        return BlockContextChangeList

    def get_preserved_filters(self, request):
        """
        Returns the preserved filters querystring.
        """
        match = request.resolver_match
        if self.preserve_filters and match:
            opts = self._meta
            info = (self._meta.app_label, self.block_type_name)
            changelist_name = '%s_%s_changelist' % info
            current_url = '%s:%s' % (match.app_name, match.url_name)
            changelist_url = 'admin:%s' % changelist_name
            if current_url == changelist_url:
                preserved_filters = request.GET.urlencode()
            else:
                preserved_filters = request.GET.get('_changelist_filters')

            if preserved_filters:
                return urlencode({'_changelist_filters': preserved_filters})
        return ''

    def changelist_view(self, request, extra_context=None):
        """
        The 'change list' admin view for this model.
        """
        from django.contrib.admin.views.main import ERROR_FLAG
        opts = self._meta
        app_label = opts.app_label
        if not self.has_change_permission(request, None):
            raise PermissionDenied

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        search_fields = self.get_search_fields(request)

        # Check actions to see if any are available on this changelist
        # actions = self.get_actions(request)
        # if actions:
        #     # Add the action checkboxes if there are any actions available.
        #     list_display = ['action_checkbox'] + list(list_display)

        ChangeList = self.get_changelist(request)
        try:
            cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                search_fields, self.list_select_related, self.list_per_page,
                self.list_max_show_all, self.list_editable, self)

        except IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given
            # and the 'invalid=1' parameter was already in the query string,
            # something is screwed up with the database, so display an error
            # page.
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        # If the request was POSTed, this might be a bulk action or a bulk
        # edit. Try to look up an action or confirmation first, but if this
        # isn't an action the POST will fall through to the bulk edit check,
        # below.
        # action_failed = False
        # selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        # Actions with no confirmation
        # TODO: Possibly implement the bulk delete.
        # Currently no actions
        # if (actions and request.method == 'POST' and
        #         'index' in request.POST and '_save' not in request.POST):
        #     if selected:
        #         response = self.response_action(request, queryset=cl.get_queryset(request))
        #         if response:
        #             return response
        #         else:
        #             action_failed = True
        #     else:
        #         msg = _("Items must be selected in order to perform "
        #                 "actions on them. No items have been changed.")
        #         self.message_user(request, msg, messages.WARNING)
        #         action_failed = True

        # # Actions with confirmation
        # if (actions and request.method == 'POST' and
        #         helpers.ACTION_CHECKBOX_NAME in request.POST and
        #         'index' not in request.POST and '_save' not in request.POST):
        #     if selected:
        #         response = self.response_action(request, queryset=cl.get_queryset(request))
        #         if response:
        #             return response
        #         else:
        #             action_failed = True

        # If we're allowing changelist editing, we need to construct a formset
        # for the changelist given all the fields to be edited. Then we'll
        # use the formset to validate/process POSTed data.
        formset = cl.formset = None

        media = self.media
        action_form = None

        # Build the action form and populate it with available actions.
        # if actions:
        #     action_form = self.action_form(auto_id=None)
        #     action_form.fields['action'].choices = self.get_action_choices(request)

        selection_note_all = ungettext('%(total_count)s selected',
            'All %(total_count)s selected', cl.result_count)

        context = dict(
            self.admin_site.each_context(request),
            module_name=force_text(self.verbose_name_plural),
            selection_note=_('0 of %(cnt)s selected') % {'cnt': len(cl.result_list)},
            selection_note_all=selection_note_all % {'total_count': cl.result_count},
            title=cl.title,
            is_popup=cl.is_popup,
            to_field=None,
            cl=cl,
            media=media,
            has_add_permission=self.has_add_permission(request),
            opts=opts,
            action_form=action_form,
            actions_on_top=self.actions_on_top,
            actions_on_bottom=self.actions_on_bottom,
            actions_selection_counter=self.actions_selection_counter,
            preserved_filters=self.get_preserved_filters(request),
            name=self.verbose_name
        )
        context.update(extra_context or {})

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.change_list_template or [
            'admin/%s/%s/block_change_list.html' % (app_label, self\
                    .block_type_name),
            'admin/%s/block_change_list.html' % app_label,
            'admin/block_change_list.html'
        ], context)


class BlockAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super(BlockAdmin, self).__init__(model, admin_site)
        opts = model._meta
        app_label = opts.app_label
        changeform_templates = [
            "admin/%s/%s/block_change_form.html" % (app_label, opts.model_name),
            "admin/%s/block_change_form.html" % app_label,
            "admin/block_change_form.html"
        ]
        if not self.add_form_template:
            self.add_form_template = changeform_templates
        if not self.change_form_template:
            self.change_form_template = changeform_templates

    def get_changelist(self,request):
        """
        Uses ReusableBlockChangeList for any block that extends ReusableBlock
        this changelist filters any blocks where can_reuse attrib is False
        """
        if not IS_POPUP_VAR in request.GET:
            raise PermissionDenied
        if issubclass(self.model, ReusableBlock):
            from clubhouse.core.views.admin import ReusableBlockChangeList
            return ReusableBlockChangeList
        return super(BlockAdmin,self).get_changelist(request)

    def in_menu(self):
        """
        Blocks should not appear in the admin menu
        """
        return False

    def get_fields(self, request, obj=None):
        fields = super(BlockAdmin,self).get_fields(request,obj)
        if not IS_POPUP_VAR in request.GET:
            try:
                del fields[fields.index('can_reuse')]
            except (IndexError, ValueError):
                pass
        return fields

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if issubclass(obj.__class__,ReusableBlock) and not IS_POPUP_VAR in\
                request.GET:
            obj.can_reuse = True

        if not obj.pk:
            obj.user_created = request.user
        else:
            obj.user_updated = request.user

        super(BlockAdmin,self).save_model(request, obj, form, change)

    def changeform_view(self, request, object_id=None, form_url='',
            extra_context=None):
        # Overritten to not show the 'save' button
        return super(BlockAdmin,self).changeform_view(request, object_id,
                form_url, {'show_save': False})


class BlockInline(GenericStackedInline):
    allow_add = True
    sortable_field_name = 'order'
    extra = 0;
    autocomplete_lookup_fields = {
        "generic": [["block_type", "block_id"]],
    }

    ct_field = 'parent_type'
    ct_fk_field = 'parent_id'

    def get_block_models(self):
        return self.model.get_block_models()

    def get_block_type_queryset(self,db):
        qry = None
        for m in self.get_block_models():
            try:
                admin_url(m, 'add')
            except NoReverseMatch:
                continue

            q = models.Q(app_label=m._meta.app_label) & \
                models.Q(model=m._meta.object_name.lower())

            qry = qry | q if qry else q

        # If qry has not been set, i.e. no blocks extend the block_type, or
        # Blocks do not have an admin, then exclude all content types..
        return ContentType.objects.filter(qry).using(db) if qry else \
                ContentType.objects.exclude(pk__gte=0)

    def get_field_queryset(self, db, db_field, request):
        block_type_re = re.compile('^[a-z_.]+\.block_type$', flags=re.I | re.U)
        if block_type_re.match(unicode(db_field)):
            return self.get_block_type_queryset(db)
        return super(BlockInline, self).get_field_queryset(db, db_field, request)


class PageAdmin(mezzanine_PageAdmin):
    def has_add_permission(self,request):
        if IS_POPUP_VAR in request.GET:
            return False
        return super(PageAdmin,self).has_add_permission(request)

    def changelist_view(self, request, extra_context=None):
        """
        Redirect to the ``Page`` changelist view for ``Page``
        subclasses.
        """
        # If this is a popup, then return the admin.ModelAdmin changelist view
        if IS_POPUP_VAR in request.GET:
            opts = self.model._meta
            app_label = opts.app_label

            self.change_list_template = [
                'admin/%s/%s/change_list.html' % (app_label, opts.model_name),
                'admin/%s/change_list.html' % app_label,
                'admin/change_list.html'
            ]
            return admin.ModelAdmin.changelist_view(self,request,extra_context)

        return super(PageAdmin, self).changelist_view(request, extra_context)


class FileBrowseImageCroppingMixin(ImageCroppingMixin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        crop_fields = getattr(self.model, 'crop_fields', {})
        if db_field.name in crop_fields:
            try:
                attrs = kwargs['widget'].attrs
            except (KeyError,AttributeError):
                attrs = {}

            target = crop_fields[db_field.name]
            if target['fk_field']:
                # it's a ForeignKey
                kwargs['widget'] = img_widgets.CropForeignKeyWidget(
                    db_field.rel,
                    field_name=target['fk_field'],
                    admin_site=self.admin_site,
                )
            elif target['hidden']:
                # it's a hidden ImageField
                kwargs['widget'] = img_widgets.HiddenImageCropWidget
            else:
                # it's a regular ImageField
                kwargs['widget'] = widgets.FileBrowseImageCropWidget(attrs=attrs)

        return super(ImageCroppingMixin, self)\
                .formfield_for_dbfield(db_field, **kwargs)


class SerializerRegistry(object):
    """
    SerializerRegistry - Used to register serializers against models,
    generally for use with blocks, but is not limiting.

    Implemented in a similar way to admin registry, in that serializer
    modules are autoloaded from installed_apps, and so you should import
    the `registry` var into your serializers module to register serializers
    """
    def __init__(self):
        self._registry = {}

    def add(self, serializer):
        try:
            model = serializer.Meta.model
        except AttributeError:
            raise TypeError('Serializer %s doesn\'t have a Meta.model '
                    'assignment' % serializer)

        model = ensure_model(model)

        if model in self._registry.keys():
            raise AlreadyRegistered('Model: %s Already registered' % model)

        self._registry[model] = serializer

    def remove(self, model):
        model = ensure_model(model)
        try:
            del self._registry[model]
        except KeyError:
            raise NotRegistered('Model %s is not registered' % model)

    def find_for_model(self, model):
        model = ensure_model(model)
        try:
            return self._registry[model]
        except KeyError:
            raise NotRegistered('Model %s is not registered' % model)


serializer_registry = SerializerRegistry()
def autodiscover_serializers():
    autodiscover_modules('serializers', register_to=serializer_registry)
