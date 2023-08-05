# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from django.conf import settings

# Admin Site Title
ADMIN_HEADLINE = getattr(settings, "CLUBHOUSE_ADMIN_HEADLINE", 'Clubhouse')
ADMIN_TITLE = getattr(settings, "CLUBHOUSE_ADMIN_TITLE", 'Clubhouse')

BLOCK_MENU_SECTION = getattr(settings,'CLUBHOUSE_BLOCK_MENU_SECTION','Block Admin')
BLOCK_MENU_INDEX = getattr(settings,'CLUBHOUSE_BLOCK_MENU_INDEX',None)

# Link to your Main Admin Site (no slashes at start and end)
# not needed anymore
ADMIN_URL = getattr(settings, "CLUBHOUSE_ADMIN_URL", '/admin/')

# Autocomplete Limit
AUTOCOMPLETE_LIMIT = getattr(settings, "CLUBHOUSE_AUTOCOMPLETE_LIMIT", 10)
# Alternative approach to define autocomplete search fields
AUTOCOMPLETE_SEARCH_FIELDS = getattr(settings, "CLUBHOUSE_AUTOCOMPLETE_SEARCH_FIELDS", {})

# SWITCH_USER: Set True in order to activate this functionality
SWITCH_USER = getattr(settings, "CLUBHOUSE_SWITCH_USER", False)
# SWITCH_USER_ORIGINAL: Defines if a user is allowed to login as another user.
# Gets a user object and returns True/False.
SWITCH_USER_ORIGINAL = getattr(settings, "CLUBHOUSE_SWITCH_USER_ORIGINAL", lambda user: user.is_superuser)
# SWITCH_USER_ORIGINAL: Defines if a user is a valid target.
# Gets a user object and returns True/False.
SWITCH_USER_TARGET = getattr(settings, "CLUBHOUSE_SWITCH_USER_TARGET", lambda original_user, user: user.is_staff and not user.is_superuser)

# CLEAN INPUT TYPES
# Replaces input types: search, email, url, tel, number, range, date
# month, week, time, datetime, datetime-local, color
# due to browser inconsistencies.
# see see https://code.djangoproject.com/ticket/23075
CLEAN_INPUT_TYPES = getattr(settings, "CLUBHOUSE_CLEAN_INPUT_TYPES", True)


