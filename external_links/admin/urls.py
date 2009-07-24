from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('external_links.admin.views',
    url(r'^top/$',
        'top_links', name='external_link_top_links'),
)
