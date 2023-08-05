# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'views.index', name='index'),
    url(r'^(?P<slug>[\w-.])/', 'views.media_stream_detail', name='media_stream_detail')
)
