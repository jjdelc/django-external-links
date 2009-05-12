# -*- coding: utf-8 -*-

"""
    External links template tags
"""

import re

from urllib import urlencode

from django.template import Library, Node
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

    return redirect_endpoint + '?' +  params


@register.tag(name='externalblock')
def do_external_block(parser, token):
    node_list = parser.parse(('endexternalblock'))
    parser.delete_first_token()
    return ExternalLink(node_list)
    

EXTLINKS = re.compile(r'''href="(?P<link>http[^>"]*)"''')

class ExternalLink(Node):
    """
    Should look for any href reference and translate that link
    into an externa link redirect
    """
    def __init__(self, nodelist):
        self.nodelist = nodelist
       
    def render(self, context):
        """
        1. Split the nodes contents in pieces
        2. Translate that start with 'http' to an external link
        3. Join it all back together for printing
        """
        redirect_endpoint = reverse('external_link')
        output = self.nodelist.render(context)
        pieces = EXTLINKS.split(output)
        result = []

        for piece in pieces:
            if piece.startswith('http:/'):
                params = urlencode({'link': piece})
                result.append(redirect_endpoint + '?' + params)
            else:
                result.append(piece)

        return 'href="'.join(result)

