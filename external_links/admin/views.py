# -*- coding: utf-8 -*-

from django.db.models import Count
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.contrib.admin.views.decorators import staff_member_required

from external_links.models import LinkClick

@staff_member_required
def top_links(request):
    summary = \
    LinkClick.objects.values('link').annotate(Count('link')).order_by('-link__count')

    return object_list(request, summary, 
        template_name='external_links/links_report.html')
    
