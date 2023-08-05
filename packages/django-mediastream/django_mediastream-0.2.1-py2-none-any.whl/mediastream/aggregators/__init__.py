# -*- coding: utf-8 -*-
from collections import namedtuple

MediaItem = namedtuple('MediaItem', [
    'service_identifier',
    'title',
    'description',
    'date_taken',
    'longitude',
    'latitude',
    'user',
    'license',
    'tags',
    'media_url',
    'media_height',
    'media_width',
    'media_type',
    'service_url',
])

SearchResult = namedtuple('SearchResult', [
    'items',
    'success',
    'message',
])


class BaseServiceAPI(object):
    """
    Base implementation of a service
    """
    def __init__(self):
        """
        Init should raise an ImproperlyConfigured exception if something isn't
        set up correctly.
        It shouldn't take any arguments
        """
        pass

    def _get_timestamp(self, dt):
        """
        Convert a datetime into a timestamp
        """
        from datetime import datetime, date

        if isinstance(dt, (datetime, date)):
            return int((dt - datetime(1970, 1, 1)).total_seconds())
        elif isinstance(dt, basestring):
            new_dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            return int((new_dt - datetime(1970, 1, 1)).total_seconds())
        return int((datetime.now() - datetime(1970, 1, 1)).total_seconds())

    def search(self, terms, term_join="AND", media_types=None, since=None):
        """
        terms: a list of strings
        term_join: the method that the terms are joined for search
        media_types: a list of string media types to narrow the search. None is all.
        since: if not None, search since this date/time

        returns: A list of MediaItem objects
        """
        raise NotImplemented
