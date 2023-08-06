# -*- coding: utf-8 -*-

from django.contrib import admin

from glitter import block_admin
from glitter.admin import GlitterAdminMixin, GlitterPagePublishedFilter

from .models import Category, LatestNewsBlock, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Post)
class PostAdmin(GlitterAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'author', 'date', 'image', 'summary',)
        }),
        ('Advanced options', {
            'fields': ('published', 'slug',)
        }),
    )
    date_hierarchy = 'date'
    list_display = ('title', 'date', 'category', 'is_published')
    list_filter = (GlitterPagePublishedFilter, 'date', 'category')
    prepopulated_fields = {
        'slug': ('title',)
    }


block_admin.site.register(LatestNewsBlock)
block_admin.site.register_block(LatestNewsBlock, 'App Blocks')
