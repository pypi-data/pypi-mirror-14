# -*- coding: utf-8 -*-

from django.contrib.admin import TabularInline
from .models import GalleryPhoto


class PhotoInline(TabularInline):
    """
    Tabular inline that will be displayed in the gallery form during frontend
    editing or in the admin site.
    """
    model = GalleryPhoto
    fk_name = "gallery"
