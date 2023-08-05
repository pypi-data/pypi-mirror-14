# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Service, MediaStream, Media, AuditLogEntry


class ServiceAdmin(admin.ModelAdmin):
    '''
    Admin View for Service
    '''
    list_display = ('name', 'module')

admin.site.register(Service, ServiceAdmin)


class MediaStreamAdmin(admin.ModelAdmin):
    '''
    Admin View for MediaStream
    '''
    list_display = ('name', 'search_terms', 'enabled', 'published')
    list_editable = ('enabled', 'published', )
    list_filter = ('services', 'enabled', 'published', )
    search_fields = ('name', 'description', )
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(MediaStream, MediaStreamAdmin)


class MediaAdmin(admin.ModelAdmin):
    '''
    Admin View for Media
    '''
    list_display = ('title', 'date_taken', 'service', 'media_type', 'visible')
    list_filter = ('service', 'media_type', 'visible')
    list_editable = ('visible', )
    search_fields = ('title', 'description')

admin.site.register(Media, MediaAdmin)


class AuditAdmin(admin.ModelAdmin):
    '''
        Admin View for Audit
    '''
    list_display = ('service', 'media_stream', 'last_ran', 'success')
    list_filter = ('service', 'media_stream', 'success')
    read_only_fields = ('service', 'media_stream', 'last_ran', 'success', 'info')

admin.site.register(AuditLogEntry, AuditAdmin)
