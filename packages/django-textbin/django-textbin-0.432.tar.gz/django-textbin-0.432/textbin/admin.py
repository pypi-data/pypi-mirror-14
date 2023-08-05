from __future__ import print_function, division, absolute_import, unicode_literals

from django.contrib import admin
from django.template.defaultfilters import truncatechars
from django.db.models import Count

from . import models

# from utils.decorator import attrs
# ToDo: find utils package!


def attrs(**kwargs):
    def attrsetter(function):
        for key, value in kwargs.items():
            setattr(function, key, value)
        return function
    return attrsetter


class MediaInline(admin.TabularInline):  # StackedInline | TabularInline
    model = models.Media
    extra = 0


@admin.register(models.Text)
class TextAdmin(admin.ModelAdmin):
    class HasAttachments(admin.SimpleListFilter):
        title = 'attachments'
        parameter_name = 'has_attachments'

        def lookups(self, request, model_admin):
            return (
                ('1', 'With attachments'),
                ('0', 'No attachments')
            )

        def queryset(self, request, queryset):
            if self.value() == '1':
                return queryset.annotate(medias_num=Count('media')).filter(medias_num__gt=0)
            elif self.value() == '0':
                return queryset.annotate(medias_num=Count('media')).filter(medias_num=0)

    list_display = ('id', 'posted_at', 'author_name', 'text_truncated', )
    search_fields = ('id', 'author_name', 'text', )
    inlines = (MediaInline, )
    readonly_fields = ('id', 'posted_at', )
    list_filter = ('posted_at', HasAttachments, )
    ordering = ('-posted_at', )

    @staticmethod
    @attrs(short_description='text', admin_order_field='text')
    def text_truncated(obj):
        return truncatechars(obj.text, 140)


@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'posted_at', 'type', 'text', 'url')
    readonly_fields = ('id', )
    search_fields = ('id', 'url', )
    list_filter = ('text__posted_at', 'type', )
    ordering = ('-text__posted_at', )

    @staticmethod
    def posted_at(obj):
        return obj.text.posted_at
