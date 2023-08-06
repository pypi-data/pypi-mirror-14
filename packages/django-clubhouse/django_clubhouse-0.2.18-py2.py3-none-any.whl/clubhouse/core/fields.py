# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models

from filebrowser_safe.fields import FileBrowseFormField

from clubhouse.core import widgets

class FileBrowseImageField(models.ImageField):
    def __init__(self,*args,**kwargs):
        self.extensions = kwargs.pop('extensions', '')
        super(FileBrowseImageField,self).__init__(*args,**kwargs)

    def formfield(self, **kwargs):
        attrs = {}
        attrs["directory"] = self.upload_to
        attrs["extensions"] = self.extensions
        attrs["format"] = 'Image'
        defaults = {
            'form_class': FileBrowseFormField,
            'widget': widgets.FileBrowseImageWidget(attrs=attrs),
            'directory': self.upload_to,
            'extensions': self.extensions,
            'format': 'Image'
        }
        defaults.update(kwargs)
        return super(FileBrowseImageField, self).formfield(**defaults)
