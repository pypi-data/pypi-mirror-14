# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import traceback
import sys

# from celery import shared_task
# from celery.utils.log import get_task_logger
import logging
from urllib2 import HTTPError

from django.core.exceptions import ImproperlyConfigured

from flickrapi import FlickrAPI
from mediastream.settings import FLICKR_KEY, FLICKR_SECRET
from mediastream.aggregators import BaseServiceAPI, MediaItem, SearchResult

logger = logging.getLogger(__name__)


class ServiceAPI(BaseServiceAPI):
    """
    Implementation of the Flickr API
    """
    _link_url = 'http://www.flickr.com/{owner}/{id}'
    _image_url = 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg'

    PHOTOS_ONLY = 'photos'
    VIDEOS_ONLY = 'videos'
    PHOTOS_AND_VIDEOS = 'all'

    SAFE_SEARCH = 1
    MODERATE_SEARCH = 2
    RESTRICTED = 3

    LICENSES = {
        '0': "All Rights Reserved",
        '1': "CC Attribution-NonCommercial-ShareAlike License (https://creativecommons.org/licenses/by-nc-sa/2.0/)",
        '2': "CC Attribution-NonCommercial License (https://creativecommons.org/licenses/by-nc/2.0/)",
        '3': "CC Attribution-NonCommercial-NoDerivs License (https://creativecommons.org/licenses/by-nc-nd/2.0/)",
        '4': "CC Attribution License (https://creativecommons.org/licenses/by/2.0/)",
        '5': "CC Attribution-ShareAlike License (https://creativecommons.org/licenses/by-sa/2.0/)",
        '6': "CC Attribution-NoDerivs License (https://creativecommons.org/licenses/by-nd/2.0/)",
        '7': "No known copyright restrictions (https://www.flickr.com/commons/usage/)",
        '8': "United States Government Work (http://www.usa.gov/copyright.shtml)",
        '9': "Public Domain Dedication (CC0) (https://creativecommons.org/publicdomain/zero/1.0/)",
        '10': "Public Domain Mark (https://creativecommons.org/publicdomain/mark/1.0/)",
    }
    SEARCH_LICENSES = '1,2,3,4,5,6,7,8,9,10'

    TAG_MODES = {
        'OR': 'any',
        'AND': 'all',
    }

    def __init__(self):
        if FLICKR_KEY is None or FLICKR_SECRET is None:
            raise ImproperlyConfigured("'FLICKR_KEY' and 'FLICKR_SECRET' must be set in MEDIASTREAM_SETTINGS to use the Flickr service.")
        self._api = FlickrAPI(FLICKR_KEY, FLICKR_SECRET)
        self._messages = []
        self._success = True
        self._items = []

    def search(self, terms, term_join="OR", media_types=None, since=None):
        """
        terms: a list of strings
        term_join: the method that the terms are joined for search
        media_types: a list of string media types to narrow the search. None is all.
        since: if not None, search since this date/time

        returns: (A list of Media objects created, log messages)
        """
        if not isinstance(terms, basestring):
            terms = ",".join(terms)
        if media_types is not None:
            include_photos = True in ['image' in x for x in media_types]
            include_video = True in ['video' in x for x in media_types]
            if include_photos and include_video:
                content_type = self.PHOTOS_AND_VIDEOS
            elif include_photos:
                content_type = self.PHOTOS_ONLY
            else:
                content_type = self.OTHERS_ONLY
        else:
            content_type = self.PHOTOS_AND_VIDEOS

        flickr_kwargs = {
            'tags': terms,
            'media': content_type,
            'safe_search': self.MODERATE_SEARCH,
            'per_page': 5,
            'tag_mode': self.TAG_MODES[term_join],
            'sort': 'date-posted-asc',
            'license': self.SEARCH_LICENSES,
            'extras': ','.join([
                'description',
                'date_taken',
                'owner_name',
                'o_dims',
                'url_o',
                'geo',
                'tags',
                'license',
                'media',
                'original_format',
            ]),
        }
        if since is not None:
            flickr_kwargs['min_taken_date'] = self._get_timestamp(since)
        else:
            flickr_kwargs['min_taken_date'] = self._get_timestamp(datetime.now() - timedelta(days=7))

        try:
            resp = self._api.photos_search(**flickr_kwargs)
            photos, = resp
            if photos.attrib['pages'] == '0':
                self._messages.append('FLICKR did that thing where it returned 0 pages')

            success_item_count = 0
            error_item_count = 0
            for photo in photos:
                try:
                    self._items.append(self._parse_media(photo))
                    success_item_count += 1
                except Exception as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error_item_count += 1
                    self._success = False
                    self._messages.append('Photo parse error: {}'.format(e))
                    self._messages.extend(traceback.format_tb(exc_traceback))
                    continue
            self._messages.append("Successfully processed {} items.".format(success_item_count))
            if error_item_count:
                self._messages.append("Errors processing {} items.".format(error_item_count))
        except HTTPError as e:
            self._success = False
            self._messages.append('returned HTTP Error {}'.format(e.code))

        return SearchResult(items=self._items, success=self._success, message="\r".join(self._messages))

    def _parse_media(self, photo):
        photodict = dict(photo.attrib)
        photodict['description'] = "".join(photo.find('description').itertext())
        if photodict['longitude'] == '0' and photodict['latitude'] == '0':
            photodict['longitude'] = None
            photodict['latitude'] = None
        else:
            float(photodict['longitude'])
            float(photodict['latitude'])
        print photodict
        return MediaItem(
            service_identifier=photodict['id'],
            title=photodict['title'][:255],
            description=photodict['description'],
            date_taken=datetime.strptime(photodict['datetaken'].encode('utf-8'), '%Y-%m-%d %H:%M:%S'),
            longitude=photodict['longitude'],
            latitude=photodict['latitude'],
            user=photodict['ownername'],
            license=self.LICENSES.get(photodict['license'], 'Unknown'),
            tags=photodict['tags'],
            media_url=self._image_url.format(**photodict),
            media_height=int(photodict.get('height_o', 0)),
            media_width=int(photodict.get('width_o', 0)),
            media_type=self._get_media_type(photodict),
            service_url=self._link_url.format(**photodict),
        )

    def _get_media_type(self, photodict):
        """
        Return a MIME type for a given item
        """
        bits = []
        if photodict['media'] == 'photo':
            bits.append('image')
        else:
            bits.append(photodict['media'])
        if photodict['originalformat'] == 'jpg':
            bits.append('jpeg')
        else:
            bits.append(photodict['originalformat'])
        return "/".join(bits)
