# -*- coding: utf-8 -*-

"""
    External links template tags
"""

from urllib import urlencode

from django.template import Library
from django.core.urlresolvers import reverse

register = Library()

@register.simple_tag
def external(link):
    """
    Replaces an external link with a redirect to
    keep track of the clicked link
    """
    redirect_endpoint = reverse('external_link')
    params = urlencode({'link': link})

    return redirect_endpoint + params
