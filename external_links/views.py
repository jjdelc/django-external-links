# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect

from external_links.models import LinkClick

def external_link(request):
    """
    Redirects links and keeps track of them
    """
    try:
        link = request.GET['link']
        link_click = LinkClick(link=link)
        link_click.store(request)
    except KeyError:
        # Someone got here without the link param
        # Redirect to Home as default
        link = '/'

    return HttpResponseRedirect(link)
