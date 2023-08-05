# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from mezzanine.utils.conf import set_dynamic_settings as mezzanine_dynamic

__all__ = ['set_dynamic_settings']

def set_dynamic_settings(s):
    mezzanine_dynamic(s)

    tuple_list_settings = ["INSTALLED_APPS"]
    for setting in tuple_list_settings[:]:
        if not isinstance(s.get(setting, []), list):
            s[setting] = list(s[setting])
        else:
            # Setting is already a list, so we'll exclude it from
            # the list of settings we'll revert back to tuples.
            tuple_list_settings.remove(setting)

    # Moves an existing list setting value to a different position.
    move = lambda n, k, i: s[n].insert(i, s[n].pop(s[n].index(k)))
    # Add a value to the end of a list setting if not in the list.
    append = lambda n, k: s[n].append(k) if k not in s[n] else None
    # Add a value to the start of a list setting if not in the list.
    prepend = lambda n, k: s[n].insert(0, k) if k not in s[n] else None
    # Insert a value into a list setting
    insert = lambda n, k, i: s[n].insert(i, k) if k not in s[n] else None
    # Remove a value from a list setting if in the list.
    remove = lambda n, k: s[n].remove(k) if k in s[n] else None

    # Try append the django.contrib.admin app
    # This is requried for some of the utilities i.e. templatetags
    append('INSTALLED_APPS','django.contrib.admin')

    # These apps will get put to the top of the list in the order defined here
    # Will be added if not already in the list.
    priority_apps = ['clubhouse.core']

    for i,app in enumerate(priority_apps):
        try:
            move('INSTALLED_APPS',app,i)
        except ValueError:
            insert('INSTALLED_APPS',app,i)

    # These apps will be moved to after the priority_apps if they are installed
    optional_apps = ['clubhouse.contrib']
    for i,app in enumerate(optional_apps):
        if app in s['INSTALLED_APPS']:
            move('INSTALLED_APPS',app,(len(priority_apps)+i))

    # Revert tuple settings back to tuples.
    for setting in tuple_list_settings:
        s[setting] = tuple(s[setting])
