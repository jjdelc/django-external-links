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

    To be used as:
        {% external "http://google.com/" %}

    """
    redirect_endpoint = reverse('external_link')
    params = urlencode({'link': link})

    return redirect_endpoint + '?' +  params


@register.tag(name='externalblock')
def do_external_block(parser, token):
    """
    {% externalblock %}
    text with <a href="">content</a> to be converted to external
    links
    {% endexternalblock %}
    """
    bits = token.split_contents()[::-1]
    tag_name = bits.pop()
    prefix = ''
    if bits:
        prefix = bits.pop()
    node_list = parser.parse(('endexternalblock'))
    parser.delete_first_token()
    return ExternalLink(node_list, prefix)
    

EXTLINKS = re.compile(r'''href="(?P<link>http[^>"]*)"''')

class ExternalLink(Node):
    """
    Should look for any href reference and translate that link
    into an externa link redirect
    """
    def __init__(self, nodelist, prefix=''):
        self.nodelist = nodelist
        self.prefix = prefix


    def replace_links(self, original_text):
        """
        Here's all the magic
            1. Split the nodes contents in pieces
            2. Translate that start with 'http' to an external link
            3. Join it all back together for printing
        """
        redirect_endpoint = self.prefix + reverse('external_link')
        pieces = EXTLINKS.split(original_text)
        result = []

        for piece in pieces:
            if piece.startswith('http:/'):
                params = urlencode({'link': piece})
                result.append('href="' + redirect_endpoint + '?' + params + '"')
            else:
                result.append(piece)

        return ''.join(result)

       
    def render(self, context):
        output = self.nodelist.render(context)
        return self.replace_links(output)

