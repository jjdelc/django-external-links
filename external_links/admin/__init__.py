# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Count
from django.conf.urls.defaults import patterns, url
from django.views.generic.list_detail import object_list

from external_links.models import LinkClick

class LinkClickAdmin(admin.ModelAdmin):
    search_fields = ('link', 'referer', 'ip_addr' )
    date_hierarchy = 'date'
    list_filter = ('site', )
    list_display = ('link', 'referer', 'ip_addr', 'date', 'time')

    change_list_template = 'external_links/change_list.html'

    def top_links(self, request):
        """
        This view shows the top clicked external links
        """
        summary = LinkClick.objects.values('link').annotate(
            Count('link')).order_by('-link__count')

        return object_list(request, summary, 
            template_name='external_links/top_links.html')
 

    def get_urls(self):
        urls = super(LinkClickAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^top/$', 
                self.admin_site.admin_view(self.top_links),
                name='external_link_top_clicks')
        )
        
        return my_urls + urls


