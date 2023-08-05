# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType

from mezzanine.conf import settings
from mezzanine.forms.signals import form_invalid, form_valid
from mezzanine.pages.page_processors import processor_for
from mezzanine.utils.email import split_addresses, send_mail_template
from mezzanine.utils.views import is_spam

from clubhouse.forms.forms import FormForForm
from clubhouse.contrib.models.pages import ModularPage


def format_value(value):
    """
    Convert a list into a comma separated string, for displaying
    select multiple values in emails.
    """
    if isinstance(value, list):
        value = ", ".join([v.strip() for v in value])
    return value

@processor_for(ModularPage)
def modularpage_processor(request, page):
    formblock_ct = ContentType.objects.get(app_label='clubhouse_forms',\
            model='formblock')

    formblocks = page.modularpage.content_blocks.filter(block_type=formblock_ct)
    from clubhouse.forms import Initialised

    for formblock in formblocks:
        registry_key = 'form:%s' % formblock.block_object.pk
        form_model = formblock.block_object.form
        form = FormForForm(formblock.block_object.form, RequestContext(request),
                           None, None)

        post_data = request.POST or {}
        if form.submit_key in post_data:
            form = FormForForm(formblock.block_object.form,
                    RequestContext(request), request.POST, request.FILES or None)

        if form.is_valid():
            url = page.get_absolute_url()
            if is_spam(request, form, url):
                return redirect(url)
            attachments = []
            for f in form.files.values():
                f.seek(0)
                attachments.append((f.name, f.read()))
            entry = form.save()
            subject = form_model.email_subject
            if not subject:
                subject = "%s - %s" % (form_model.title, entry.entry_time)
            fields = [(v.label, format_value(form.cleaned_data[k]))
                      for (k, v) in form.fields.items()]
            context = {
                "fields": fields,
                "message": form_model.email_message,
                "request": request,
            }
            email_from = form_model.email_from or settings.DEFAULT_FROM_EMAIL
            email_to = form.email_to()
            if email_to and form_model.send_email:
                send_mail_template(subject, "email/form_response", email_from,
                                   email_to, context)
            headers = None
            if email_to:
                # Add the email entered as a Reply-To header
                headers = {'Reply-To': email_to}
            email_copies = split_addresses(form_model.email_copies)
            if email_copies:
                send_mail_template(subject, "email/form_response_copies",
                                   email_from, email_copies, context,
                                   attachments=attachments, headers=headers)
            form_valid.send(sender=request, form=form, entry=entry)
            form.is_submitted = True
        else:
            form_invalid.send(sender=request, form=form)

        Initialised.register(registry_key, form)

    return {}


