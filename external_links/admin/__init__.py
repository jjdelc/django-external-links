# -*- coding: utf-8 -*-

from django.contrib import admin

from external_links.models import LinkClick

class LinkClickAdmin(admin.ModelAdmin):
    search_fields = ('link', 'referer', 'ip_addr' )
    date_hierarchy = 'date'
    list_filter = ('site', )
    list_display = ('link', 'referer', 'ip_addr', 'date', 'time')
