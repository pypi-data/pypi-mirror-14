# -*- coding: utf-8 -*-
from django.conf import settings as site_settings


DEFAULT_SETTINGS = {
    'MEDIA_TYPE_CHOICES': [
        ('image/jpeg', 'JPEG image'),
        ('image/png', 'PNG image'),
        ('video/webm', 'WebM Video'),
        ('video/mp4', 'MPEG 4 Video')
    ],
    'FLICKR_KEY': None,
    'FLICKR_SECRET': None,
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(site_settings, 'MEDIASTREAM_SETTINGS', {}))

if USER_SETTINGS['FLICKR_KEY'] is None:
    USER_SETTINGS['FLICKR_KEY'] = getattr(site_settings, 'FLICKR_KEY', None)
    USER_SETTINGS['FLICKR_SECRET'] = getattr(site_settings, 'FLICKR_SECRET', None)

globals().update(USER_SETTINGS)
