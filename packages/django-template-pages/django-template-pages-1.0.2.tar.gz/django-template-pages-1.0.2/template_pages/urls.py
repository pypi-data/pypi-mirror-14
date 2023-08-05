from django.conf.urls import url

from template_pages.views import routing_view


urlpatterns = [
    url(r'^(?P<path>[^.\n]*)/$', routing_view, name='template_pages_routing_view'),
    url(r'^$', routing_view, {'path': ''}, name='template_pages_routing_view'),
]
