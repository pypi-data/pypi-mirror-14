# coding: utf-8

# python imports
from functools import wraps
import json

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

# django imports
from django import template
from django.apps import apps
from django.template import TemplateSyntaxError,Context
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.template.loader import get_template, select_template
from django.template.context import Context
from django.utils.translation import ugettext as _
from django.contrib.admin.utils import (
    display_for_field, display_for_value, label_for_field, lookup_field,
)

from mezzanine.utils.urls import admin_url

from clubhouse.core.settings import *
from clubhouse.core.models import ReusableBlock, BlockContext

register = template.Library()


# GENERIC OBJECTS
class do_get_generic_objects(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        objects = {}
        for c in ContentType.objects.all().order_by('id'):
            klass = apps.get_model(c.app_label, c.model)
            selectable = (issubclass(klass, BlockContext) and\
                    issubclass(klass, ReusableBlock)) or\
                    not issubclass(klass,BlockContext)
            objects[c.id] = {
                'pk': c.id,
                'app': c.app_label,
                'model': c.model,
                'selectable': selectable
            }
        return json.dumps(objects)


@register.tag
def get_content_types(parser, token):
    """
    Returns a list of installed applications and models.
    Needed for lookup of generic relationships.
    """
    return do_get_generic_objects()


class do_block_type_options(template.Node):
    def __init__(self):
        pass

    def render(self, context):
         return ''.join(['<option value="%s">%s</option>' % (admin_url(m,'add'),
             m._meta.verbose_name) for m in context['cl'].model_admin\
             .collect_models()])


@register.tag
def get_block_type_options(parser, token):
    return do_block_type_options()


# ADMIN_TITLE
@register.simple_tag
def get_admin_title():
    """
    Returns the Title for the Admin-Interface.
    """
    return ADMIN_TITLE


# SITE_TITLE
@register.simple_tag
def get_site_title():
    """
    Returns the Title for the Admin-Interface.
    """
    return ADMIN_TITLE or _("Django site admin")


# RETURNS CURRENT LANGUAGE
@register.simple_tag
def get_lang():
    return get_language()


# ADMIN_URL
@register.simple_tag
def get_admin_url():
    """
    Returns the URL for the Admin-Interface.
    """
    return ADMIN_URL


@register.simple_tag
def get_date_format():
    return get_format('DATE_INPUT_FORMATS')[0]


@register.simple_tag
def get_time_format():
    return get_format('TIME_INPUT_FORMATS')[0]


@register.simple_tag
def get_datetime_format():
    return get_format('DATETIME_INPUT_FORMATS')[0]


@register.simple_tag
def clubhouse_admin_title():
    return ADMIN_TITLE


@register.simple_tag
def clubhouse_clean_input_types():
    return CLEAN_INPUT_TYPES


@register.filter
def classname(obj, arg=None):
    classname = obj.__class__.__name__.lower()
    if arg:
        if arg.lower() == classname:
            return True
        return False
    return classname


@register.filter
def classpath(obj):
    module = obj.__module__
    classname = obj.__class__.__name__
    return "%s,%s" % (module, classname)


# FORMSETSORT FOR SORTABLE INLINES

@register.filter
def formsetsort(formset, arg):
    """
    Takes a list of formset dicts, returns that list sorted by the sortable field.
    """
    if arg:
        sorted_list = []
        for item in formset:
            position = item.form[arg].data
            if position and position != "-1":
                sorted_list.append((int(position), item))
        sorted_list.sort()
        sorted_list = [item[1] for item in sorted_list]
        for item in formset:
            position = item.form[arg].data
            if not position or position == "-1":
                sorted_list.append(item)
    else:
        sorted_list = formset
    return sorted_list


# RELATED LOOKUPS

def safe_json_else_list_tag(f):
    """
    Decorator. Registers function as a simple_tag.
    Try: Return value of the decorated function marked safe and json encoded.
    Except: Return []
    """
    @wraps(f)
    def inner(model_admin):
        try:
            return mark_safe(json.dumps(f(model_admin)))
        except:
            return []
    return register.simple_tag(inner)


@safe_json_else_list_tag
def get_related_lookup_fields_fk(model_admin):
    return model_admin.related_lookup_fields.get("fk", [])


@safe_json_else_list_tag
def get_related_lookup_fields_m2m(model_admin):
    return model_admin.related_lookup_fields.get("m2m", [])


@safe_json_else_list_tag
def get_related_lookup_fields_generic(model_admin):
    return model_admin.related_lookup_fields.get("generic", [])


# AUTOCOMPLETES

@safe_json_else_list_tag
def get_autocomplete_lookup_fields_fk(model_admin):
    return model_admin.autocomplete_lookup_fields.get("fk", [])


@safe_json_else_list_tag
def get_autocomplete_lookup_fields_m2m(model_admin):
    return model_admin.autocomplete_lookup_fields.get("m2m", [])


@safe_json_else_list_tag
def get_autocomplete_lookup_fields_generic(model_admin):
    return model_admin.autocomplete_lookup_fields.get("generic", [])


# SORTABLE EXCLUDES
@safe_json_else_list_tag
def get_sortable_excludes(model_admin):
    return model_admin.sortable_excludes


@register.filter
def prettylabel(value):
    return mark_safe(value.replace(":</label>", "</label>"))


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def block_submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    ctx = {
        'opts': opts,
        # TODO: Implement deletes in an appropriate way.. so as not to leave
        # lingering model references
        'show_delete_link': False,
        # 'show_delete_link': (
        #     not is_popup and context['has_delete_permission'] and
        #     change and context.get('show_delete', True)
        # ),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': (
            context['has_add_permission'] and not is_popup and
            (not save_as or context['add'])
        ),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': is_popup,
        'preserved_filters': context.get('preserved_filters'),
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx


@register.simple_tag(takes_context=True)
def render_blocks(context, block_context, parent=None, template=None, **kwargs):
    if isinstance(block_context, basestring):
        try:
            app_label, model_name = block_context.split('.')
            block_context = apps.get_model(app_label, model_name)
        except ValueError:
            error = ('First argument to render_blocks must be the block context '
            ' model, or string in the format "app_label.ModelName"')
            raise TemplateSyntaxError(error)

    if not issubclass(block_context, BlockContext):
        error = ('block_context must be a clubhouse.core.models.BlockContext '
                'instance')
        raise TemplateSyntaxError(error)

    if not parent:
        try:
            parent = context['page'].get_content_model()
        except KeyError:
            error = ('Could not find parent for block context, please provide')
            raise TemplateSyntaxError(error)

    if not template:
        template = block_context.get_template()

    parent_ct = ContentType.objects.get_for_model(parent)
    parent_id = parent.pk

    kwargs.update({
        'blocks': block_context.objects.filter(parent_type=parent_ct,
            parent_id=parent_id).order_by('order'),
        'parent': parent,
        'context_model': block_context
    })
    return select_template([template, 'block_context.html'])\
            .render(Context(kwargs))

