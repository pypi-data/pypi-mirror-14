# -*- coding: utf-8 -*-
__author__ = "spi4ka"
from django import template
from django.conf import settings
from ..models.blogpost import BlogPost
from ..models.categories import Categories

register = template.Library()


@register.inclusion_tag('django_blogposts/list-item.html')
def blogpost_list_item(page, position="left"):
    return {
        'object': page,
        'position': position
    }


@register.inclusion_tag('django_blogposts/categories/list.html')
def categories_list(active):
    if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
        object_list = Categories.objects.filter(is_moderated=True)
    else:
        object_list = Categories.objects.none()
    
    if active:
        active = int(active)
    return { 'object_list': object_list, 'active': active }