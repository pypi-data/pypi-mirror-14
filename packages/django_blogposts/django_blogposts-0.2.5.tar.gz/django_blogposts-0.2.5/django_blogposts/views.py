# -*- coding: utf-8 -*-
__author__ = "spi4ka"
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404
from .models.blogpost import BlogPost
from .models.categories import Categories
from .models.tags import Tags
from django.conf import settings


class PostsListView(ListView):

    model = BlogPost

    model_fields = ['pk', 'header', 'short_content', 'image', 'da']

    paginate_by = 10

    template_name = "django_blogposts/list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(
            is_moderated=True
        )
        if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
            queryset = queryset.filter(
                category__is_moderated=True
            )

            if self.kwargs.get('pk'):
                queryset = queryset.filter(
                    category__pk=self.kwargs.get('pk')
                )

        if getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
            queryset = queryset.filter(
                tags__is_moderated=True
            )

            if self.request.GET.get('tag'):
                queryset = queryset.filter(
                    tags__slug=self.request.GET.get('tag')
                )

        if self.request.GET.get('q'):
            queryset = queryset.filter(
                header__icontains=self.request.GET.get('q'),
            )

        return queryset.only(*self.model_fields)

    def get_context_data(self, *args, **kwargs):
        context = super(PostsListView, self).get_context_data(*args, **kwargs)
        if self.kwargs.get('pk'):
            if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
                try:
                    context['category'] = Categories.objects.get(
                        pk=self.kwargs.get('pk')
                    )
                except Categories.DoesNotExist:
                    pass

            if getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
                context['tags'] = Tags.objects.filter(is_moderated=True)

        context['active_category'] = self.kwargs.get('pk')
        return context


class PostsDetailView(DetailView):

    model = BlogPost

    template_name = "django_blogposts/detail.html"

    def get_object(self):
        try:
            page = self.model.objects.get(pk=self.kwargs.get('pk'))
            if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
                if not page.category.is_moderated:
                    raise Http404
        except:
            raise Http404
        return page
