# -*- coding: utf-8 -*-
__author__ = "spi4ka"
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField
from .categories import Categories
from .tags import Tags

TextField = models.TextField

try:
    from ckeditor.fields import RichTextField
    TextField = RichTextField
except ImportError:
    pass


class BlogPost(models.Model):

    meta_title = models.CharField(_("Meta-tag title"), max_length=400)
    meta_kw = models.CharField(_("Meta-tag keywords"), max_length=400)
    meta_desc = models.TextField(_("Meta-tag Description"))

    slug = AutoSlugField(
        _("Slug"),
        populate_from='header',
        max_length=100,
        always_update=True
    )

    header = models.CharField(_("Header (tag H1)"), max_length=400)
    short_content = TextField(_("Short content for preview"), blank=True, null=True)
    content = TextField(_("Content"))

    image = models.ImageField(_("Image"), upload_to="blog/%Y/%m/%d", null=True, blank=True)

    is_moderated = models.BooleanField(_("Is moderated"), default=True)

    da = models.DateTimeField(_("Date of create"), auto_now_add=True)
    de = models.DateTimeField(_("Date of last edit"), auto_now=True)

    category = models.ForeignKey(
        Categories,
        verbose_name=_("category"),
        null=True,
        blank=True
    )

    tags = models.ManyToManyField(
        Tags,
        verbose_name=_("tags"),
        blank=True
    )

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"
        ordering = ['-da']

    def __unicode__(self):
        return u"{}".format(self.__str__(),)

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('django-blogposts-detail', args=(self.pk, self.slug,))

    def get_tags(self):
        return self.tags.filter(is_moderated=True)
