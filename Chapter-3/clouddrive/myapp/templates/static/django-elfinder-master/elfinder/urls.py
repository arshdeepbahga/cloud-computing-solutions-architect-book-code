from django.conf.urls.defaults import patterns, include, url
from elfinder.views import index, connector_view

urlpatterns = patterns('',
    url(r'^(?P<coll_id>\d+)/$', index, name='elfinder_index'),
    url(r'^connector/(?P<coll_id>\d+)/$', connector_view,
        name='elfinder_connector'),
)
