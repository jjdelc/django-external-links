# -*- coding: utf-8 -*-

from urllib import quote, urlencode

from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse
from django.template import Template, Context

from external_links.models import LinkClick

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
        self.assertEqual(template.render(ctx), external_url + params)
        
