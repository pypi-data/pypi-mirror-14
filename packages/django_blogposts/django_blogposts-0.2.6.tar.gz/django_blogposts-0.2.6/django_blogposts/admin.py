# -*- coding: utf-8 -*-
__author__ = "spi4ka"
from django.contrib import admin
from .models.blogpost import BlogPost
from .models.categories import Categories
from .models.tags import Tags
from django.conf import settings


post_exclude = []

if not getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
    post_exclude.append('category')
else:
    @admin.register(Categories)
    class CategoriesAdmin(admin.ModelAdmin):
        search_fields = ('name', 'slug', 'da', )
        list_filter = ['is_moderated']

if not getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
    post_exclude.append('tags')
else:
    @admin.register(Tags)
    class TagsAdmin(admin.ModelAdmin):
        search_fields = ('name', 'slug', 'da', )
        list_filter = ['is_moderated']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    search_fields = ('header', 'meta_title', 'slug', 'da', )
    list_filter = ['is_moderated']
    exclude = post_exclude
