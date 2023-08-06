# vim: ai ts=4 sts=4 et sw=4
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os

from django.conf import settings
from django.contrib.admin.templatetags import admin_static
from django import forms

from filebrowser_safe.fields import FileBrowseWidget
from filebrowser_safe.base import FileObject
from filebrowser_safe.settings import URL_FILEBROWSER_MEDIA

from image_cropping.widgets import get_attrs

class FileBrowseImageWidget(FileBrowseWidget):
    def render(self, name, value, attrs=None):
        if value:
            if not isinstance(value, basestring):
                value = FileObject(value.path.replace('%s/' % settings.MEDIA_ROOT,''))
            else:
                value = FileObject(value)
        else:
            # Ensure value is not empty string.
            value = None

        return super(FileBrowseImageWidget,self).render(name,value,attrs)


class FileBrowseImageCropWidget(FileBrowseImageWidget):
    def _media(self):
        js = [
            "image_cropping/js/jquery.Jcrop.min.js",
            "image_cropping/image_cropping.js",
            os.path.join(URL_FILEBROWSER_MEDIA, 'js/AddFileBrowser.js')
        ]
        js = [admin_static.static(path) for path in js]

        if settings.IMAGE_CROPPING_JQUERY_URL:
            js.insert(0, settings.IMAGE_CROPPING_JQUERY_URL)

        css = [
            "image_cropping/css/jquery.Jcrop.min.css",
            "image_cropping/css/image_cropping.css",
        ]
        css = {'all': [admin_static.static(path) for path in css]}

        return forms.Media(css=css, js=js)

    media = property(_media)

    def render(self, name, value, attrs=None):
        if not attrs:
            attrs = {}
        if value:
            attrs.update({k.replace('-','_'): v for k,v in \
                    get_attrs(value,name).items()})
        return super(FileBrowseImageCropWidget, self).render(name, value, attrs)
