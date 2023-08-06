# -*- coding: utf-8 -*-
__author__ = "spi4ka"
from django.contrib.sitemaps import Sitemap
from django.conf import settings
from .models.blogpost import BlogPost


class BlogPostSitemap(Sitemap):

    def items(self):
        items = BlogPost.objects.filter(is_moderated=True)
        if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
            items = items.filter(category__is_moderated=True)

        if getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
            items = items.filter(
                Q(tags__is_moderated=True) | Q(tags=None)
            )

        return items.distinct()

    def lastmod(self, obj):
        return obj.de
