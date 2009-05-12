# -*- coding: utf-8 -*-

from urllib import quote, urlencode

from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse
from django.template import Template, Context

from external_links.models import LinkClick
from external_links.templatetags.external_link_tags import ExternalLink

DESTINATION = 'http://example.com/?param=val&param2=val2'

class ExternalLinkTest(TestCase):
    """
    Test External link
    """

    def test_view(self):
        clicks_count = LinkClick.objects.filter(link=DESTINATION).count()
        client = Client()
        external_url = reverse('external_link')
        client.get(external_url, {'link': DESTINATION})
        clicks_new_count = LinkClick.objects.filter(link=DESTINATION).count()
        self.assertEqual(clicks_new_count - clicks_count, 1)

    def test_ttag(self):
        ctx = Context()
        template = Template('{%% load external_link_tags %%}'
            '{%% external "%s" %%}' % DESTINATION)
        external_url = reverse('external_link')
        params = urlencode({'link': DESTINATION})
        self.assertEqual(template.render(ctx), external_url + '?' + params)

    def test_blocktag(self):
        external_link = ExternalLink([])
        base = 'link1: <a href="%(link1)s" title="">hey</a>, <a href="%(link2)s">hoho</a> wee'

        original_text = base % {
            'link1': DESTINATION,
            'link2': DESTINATION
        } 

        external_url = reverse('external_link')
        params = urlencode({'link': DESTINATION})

        final_dest = external_url + '?' + params
        final_text = base % {
            'link1': final_dest,
            'link2': final_dest,
        }
        self.assertEqual(final_text, 
            external_link.replace_links(original_text))
