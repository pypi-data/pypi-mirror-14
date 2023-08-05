# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from itertools import chain
from operator import attrgetter

from django.contrib.admin.views.main import (
    ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR, ERROR_FLAG,
    ChangeList
)
from django.contrib.admin.options import (
    IS_POPUP_VAR, TO_FIELD_VAR, IncorrectLookupParameters,
)
from django.contrib.admin.utils import quote
from django.utils.translation import ugettext, ugettext_lazy
from django.utils.encoding import force_text
from django.core.urlresolvers import reverse


class BlockContextChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super(BlockContextChangeList,self).__init__(*args,**kwargs)
        if self.is_popup:
            title = ugettext('Select %s')
        else:
            title = ugettext('Select %s to change')
        self.title = title % force_text(self.model_admin.verbose_name)

    def get_ordering(self, request):
        """
        Returns the list of ordering fields for the change list.
        First we check the get_ordering() method in model admin, then we check
        the object's default ordering. Then, any manually-specified ordering
        from the query string overrides anything. Finally, a deterministic
        order is guaranteed by ensuring the primary key is used as the last
        ordering field.
        """
        params = self.params
        ordering = list(self.model_admin.get_ordering(request)
                        or self._get_default_ordering())
        if ORDER_VAR in params:
            # Clear ordering and used params
            ordering = []
            order_params = params[ORDER_VAR].split('.')
            for p in order_params:
                try:
                    none, pfx, idx = p.rpartition('-')
                    field_name = self.list_display[int(idx)]
                    order_field = self.get_ordering_field(field_name)
                    if not order_field:
                        continue  # No 'admin_order_field', skip it
                    # reverse order if order_field has already "-" as prefix
                    if order_field.startswith('-') and pfx == "-":
                        ordering.append(order_field[1:])
                    else:
                        ordering.append(pfx + order_field)
                except (IndexError, ValueError):
                    continue  # Invalid ordering specified, skip it.

        # Ensure that the primary key is systematically present in the list of
        # ordering fields so we can guarantee a deterministic order across all
        # database backends.
        if not (set(ordering) & {'pk', '-pk'}):
            # The two sets do not intersect, meaning the pk isn't present. So
            # we add it.
            ordering.append('-pk')

        return ordering

    def get_queryset(self, request):
        # First, we collect all the declared list filters.
        (self.filter_specs, self.has_filters, remaining_lookup_params,
         filters_use_distinct) = self.get_filters(request)

        # Then, we let every list filter modify the queryset to its liking.
        model_sets = self.root_queryset
        for m,qs in model_sets.items():
            try_filter = True
            for filter_spec in self.filter_specs:
                new_qs = filter_spec.queryset(request, qs)
                # Allow filters to return False to disclude
                if new_qs == False:
                    del model_sets[m]
                    try_filter = False
                    break

                if new_qs is not None:
                    qs = new_qs

            if try_filter == False:
                continue

            try:
                # Finally, we apply the remaining lookup parameters from the query
                # string (i.e. those that haven't already been processed by the
                # filters).
                qs = qs.filter(**remaining_lookup_params)
            except (SuspiciousOperation, ImproperlyConfigured):
                # Allow certain types of errors to be re-raised as-is so that the
                # caller can treat them in a special way.
                raise
            except Exception as e:
                # Every other error is caught with a naked except, because we don't
                # have any other way of validating lookup parameters. They might be
                # invalid if the keyword arguments are incorrect, or if the values
                # are not in the correct type, so we might get FieldError,
                # ValueError, ValidationError, or ?.
                raise IncorrectLookupParameters(e)

            if not qs.query.select_related:
                qs = self.apply_select_related(qs)

            # Set ordering.
            # No need to set ordering as ordering will be done as a collective
            # ordering = self.get_ordering(request, qs)
            # qs = qs.order_by(*ordering)

            # Apply search results
            qs, search_use_distinct = self.model_admin.get_search_results(
                request, qs, self.query)

            # Remove duplicates from results, if necessary
            if filters_use_distinct | search_use_distinct:
                model_sets[m] = qs.distinct()
            else:
                model_sets[m] = qs

        return model_sets

    def get_results(self, request):
        object_list = list(chain(*[q for m,q in self.queryset.items()]))

        paginator = self.model_admin.get_paginator(request, object_list, self.list_per_page)
        # Get the number of objects, with admin filters applied.
        result_count = paginator.count

        # Get the total number of objects, with no admin filters applied.
        # Perform a slight optimization:
        # full_result_count is equal to paginator.count if no filters
        # were applied
        if self.model_admin.show_full_result_count:
            if self.get_filters_params() or self.params.get(SEARCH_VAR):
                full_result_count = len(object_list)
            else:
                full_result_count = result_count
        else:
            full_result_count = None
        can_show_all = result_count <= self.list_max_show_all
        multi_page = result_count > self.list_per_page

        # Get the list of objects to display on this page.
        if (self.show_all and can_show_all) or not multi_page:
            result_list = object_list
        else:
            try:
                result_list = paginator.page(self.page_num + 1).object_list
            except InvalidPage:
                raise IncorrectLookupParameters

        # Apply ordering in reverse order to maintain ordering presedence
        # TODO: apply sorting on just the result list, or all objects..?
        for o in self.get_ordering(request)[::-1]:
            reverse = o.startswith('-')
            o = o[1:] if reverse else o
            result_list = sorted(result_list,key=attrgetter(o), reverse=reverse)

        self.result_count = result_count
        self.show_full_result_count = self.model_admin.show_full_result_count
        # Admin actions are shown if there is at least one entry
        # or if entries are not counted because show_full_result_count is disabled
        self.show_admin_actions = not self.show_full_result_count or bool(full_result_count)
        self.full_result_count = full_result_count
        self.result_list = result_list
        self.can_show_all = can_show_all
        self.multi_page = multi_page
        self.paginator = paginator

    def url_for_result(self, result):
        pk_attname = result._meta.pk.attname
        pk = getattr(result, pk_attname)
        return reverse('admin:%s_%s_change' % (result._meta.app_label,
                                               result._meta.model_name),
                       args=(quote(pk),),
                       current_app=self.model_admin.admin_site.name)


class ReusableBlockChangeList(ChangeList):
    def get_queryset(self,request):
        qs = super(ReusableBlockChangeList,self).get_queryset(request)
        return qs.filter(can_reuse=True)
