# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    # url(r'^$', 'mediastream.views.index', name='index'),
    url(r'^(?P<slug>[-\w._]+)/', 'mediastream.views.media_stream_detail', name='media_stream_detail')
)
