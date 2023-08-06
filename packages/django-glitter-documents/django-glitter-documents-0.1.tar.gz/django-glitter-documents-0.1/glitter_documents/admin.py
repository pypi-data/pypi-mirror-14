# -*- coding: utf-8 -*-

from django.contrib import admin

from glitter import block_admin
from glitter.admin import GlitterAdminMixin

from .models import Category, Document, Format, LatestDocumentsBlock


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    search_fields = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Document)
class DocumentAdmin(GlitterAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ('Document', {
            'fields': (
                'title', 'category', 'author', 'document', 'document_format', 'summary',
            )
        }),
        ('Advanced options', {
            'fields': ('slug',)
        }),
    )
    date_hierarchy = 'created_at'
    list_display = ('title', 'category', 'document_format', 'file_size',)
    list_filter = ('category',)
    prepopulated_fields = {
        'slug': ('title',)
    }


block_admin.site.register(LatestDocumentsBlock)
block_admin.site.register_block(LatestDocumentsBlock, 'App Blocks')
