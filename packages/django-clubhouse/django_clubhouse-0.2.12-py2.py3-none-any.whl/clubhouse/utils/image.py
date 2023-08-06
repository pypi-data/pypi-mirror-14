# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import os
import math
import re

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.core.files import File
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.encoding import force_text
from django.utils.translation import (
    get_language as active_language, activate as activate_lang
)
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.text import capfirst, slugify, Truncator
from django.core.files.storage import default_storage

from image_cropping.fields import ImageRatioField
from imagekit.models.fields import ProcessedImageField
try:
    from filebrowser_safe.base import FileObject
except ImportError:
    class FileObject(object):
        pass

from PIL import Image, ImageDraw, ImageOps
from pilkit.processors import ResizeToFit, ResizeToFill
from six import BytesIO

from clubhouse.utils.models import have_fields_changed

logger = logging.getLogger(__name__)

IMAGE_QUALITY = getattr(settings, 'CROP_IMAGE_QUALITY', 95)


class ImageCropHelper(object):
    """
    Model Mixin for Image cropping
    """
    _image_sizes = settings.IMAGE_CROP_SIZES

    @classmethod
    def make_autocropping_field(cls, width, height, upload_to="images", processor="fit", image_format="JPEG", matte_colour=(255, 255, 255, 255), **kwargs):
        """
        Creates an imagekit.models.fields.ProcessedImageField that automatically scales and crops images
        """
        assert processor in ("fit", "fill"), "invalid processor"
        if processor == "fill":
            processors = [ResizeToFill(width, height)]
        else:
            processors = [ResizeToFit(width, height, mat_color=matte_colour)]

        assert image_format in ("JPEG", "PNG"), "invalid image_format"
        if image_format == "PNG":
            image_options = {"optimize": True}
        else:
            image_options = {"quality": IMAGE_QUALITY}

        help_text = "Automatically scaled to %s×%s" % (width, height)
        help_text_additional = kwargs.pop("help_text", None)
        if help_text_additional:
            help_text = "%s. %s" % (help_text_additional, help_text)

        return ProcessedImageField(
            processors=processors,
            format=image_format,
            options=image_options,
            upload_to=upload_to,
            help_text=help_text,
            **kwargs
        )

    @classmethod
    def make_cropping_field(cls, size_key, origin_field_name="image", verbose_name=None, help_text=None):
        """
        Creates a image_cropping.fields.ImageRatioField that allows cropping of images in the admin forms.
        NB: make sure to call self.crop_image_if_needed in the save method of models using these fields
        """
        size = cls._image_sizes[size_key]
        if not verbose_name:
            verbose_name = " ".join(map(capfirst, size_key.split("_")))
            verbose_name = "%s crop" % verbose_name
        if not help_text:
            help_text = "Crops image to %s×%s" % (size[0], size[1])
        return ImageRatioField(
            image_field=origin_field_name,
            size="%sx%s" % (size[0], size[1]),
            size_warning=True,
            verbose_name=verbose_name,
            help_text=help_text,
        )

    @classmethod
    def _crop_image(cls, origin_image, target_image, size, crop_box, image_format="JPEG"):
        """
        Resizes an image from one model field and saves into another
        :param origin_image: django.db.models.fields.files.ImageFieldFile
        :param target_image: django.db.models.fields.files.ImageFieldFile
        :param size: tuple of final desired width and height
        :param crop_box: str, 4-coordinate crop box
        :param image_format: str, Pillow Image format
        """
        # Original photo
        origin_image.seek(0)
        image_file = Image.open(origin_image)

        # Convert to RGB
        if image_file.mode not in ("L", "RGB"):
            image_file = image_file.convert("RGB")

        if crop_box:
            try:
                values = [int(x) for x in crop_box.split(",")]
                width = abs(values[2] - values[0])
                height = abs(values[3] - values[1])
                if width and height and (width != image_file.size[0] or height != image_file.size[1]):
                    image_file = image_file.crop(values)
            except (ValueError, TypeError, IndexError):
                # There's garbage in the cropping field, ignore
                print("Unable to parse crop_box parameter value '%s'. Ignoring." % crop_box)

        image_file = ImageOps.fit(image_file, size, method=Image.LANCZOS)
        image_content = BytesIO()
        image_file.save(image_content, format=image_format, quality=IMAGE_QUALITY)
        image_content = ImageFile(image_content, origin_image.name)
        target_image.save(name=image_content.name, content=image_content, save=False)

    def crop_image_if_needed(self, size_key, origin_field_name="image", target_field_name=None, crop_field_name=None,force_resize=False):
        """
        Crops an ImageField into another using an ImageRatioField
        :param size_key: str, standard image size name
        :param origin_field_name: name of origin ImageField, usually "image"
        :param target_field_name: name of target ImageField, normally inferred from size_key
        :param crop_field_name: name of ImageRatioField, normally inferred from size_key
        """
        target_field_name = target_field_name or "%s_image" % size_key
        crop_field_name = crop_field_name or "%s_crop" % size_key

        origin_image = getattr(self, origin_field_name)
        has_unsaved_image = not self.pk and origin_image
        if force_resize or has_unsaved_image or have_fields_changed(self, origin_field_name, crop_field_name):
            size = self._image_sizes[size_key]
            target_image = getattr(self, target_field_name)
            crop_box = getattr(self, crop_field_name)
            # print("cropping %s" % size_key)
            self._crop_image(origin_image, target_image, size, crop_box)

