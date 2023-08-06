
from django.conf.urls import patterns, url

from .views import NoosferoProxyView


# Noosfero URLs
urlpatterns = patterns('',
                       url(r'^(?P<path>.*)$', NoosferoProxyView.as_view(),
                           name='noosfero'),)
