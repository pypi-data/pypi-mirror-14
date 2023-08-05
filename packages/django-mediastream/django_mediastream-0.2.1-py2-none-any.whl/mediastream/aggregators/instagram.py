#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from base64 import b64encode
from urlparse import urlsplit, parse_qs
from time import sleep
try:
    import cPickle as pickle
except ImportError:
    import pickle

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from instagram import InstagramAPI, InstagramAPIError, InstagramClientError
from pytz import utc

from images.models import Image
from aggregation.models import Source, Log


api = InstagramAPI(client_id=settings.INSTAGRAM_CLIENT_ID,
                   client_secret=settings.INSTAGRAM_CLIENT_ID)
task_logger = get_task_logger(__name__)


def parse_photo(photo):
    # since the tagged feed is sorted by date tagged and an image could be
    # tagged by any comment, we need to find the latest date possible
    times = [photo.created_time]
    if photo.caption:
        times.append(photo.caption.created_at)
    times.extend(c.created_at for c in photo.comments)
    max_time = max(times)

    if photo.comments:
        tagged_at = photo.comments[-1].created_at
    return Image(
            upstream_url=photo.link,
            image_url=photo.get_standard_resolution_url(),
            source=Source.get_by_name('Instagram'),
            description=photo.caption.text if photo.caption else '',
            user=photo.user.username,
            date_uploaded=utc.localize(max_time),
            geolocation=geometry.Point(x=float(photo.location.point.longitude),
                                       y=float(photo.location.point.latitude),
                                       srid=4326)
                 if hasattr(photo, 'location') and photo.location.point
                 else geometry.Point(0, 0, srid=4326),
            original={'pickle': b64encode(pickle.dumps(photo))},
            ), [t.name for t in photo.tags] if hasattr(photo, 'tags') else []


@shared_task
def collect():
    logger = Log.new(task_logger, 'instagram', None, False)
    try:
        _collect(logger)
    except Exception as e:
        logger.error('instagram exception: {}'.format(e))
    logger.save_and_cleanup()


def _collect(logger):
    try:
        latest = Image.objects.filter(source__name='Instagram').latest().date_uploaded
    except Image.DoesNotExist:
        latest = settings.AGGREGATION_START_DATE

    max_id = None
    count = 0
    while True:
        logger.debug('INSTAGRAM next_max_id = {}'.format(max_id))
        try:
            media, next_ = api.tag_recent_media(tag_name=settings.INSTAGRAM_TAG,
                                                max_tag_id=max_id)
            logger.add_url('instagram:// tag_name={}, max_tag_id={}'.format(settings.INSTAGRAM_TAG, max_id))
        except InstagramClientError as e:
            if e.error_message != 'Unable to parse response, not valid JSON.':
                raise
            logger.warn('INSTAGRAM returned invalid JSON')
            continue
        except InstagramAPIError as e:
            if e.error_type != 'Rate limited':
                raise
            logger.warn('INSTAGRAM Rate limit hit')
            sleep(1)
            continue
        for photo in media:
            image, tags = parse_photo(photo)
            logger.debug('INSTAGRAM image.date_uploaded={}, latest={}'.format(
                image.date_uploaded, latest))
            if image.date_uploaded <= latest:
                logger.info('INSTAGRAM {} images ingested'.format(count))
                return

            # The way instagram returns tags means we get the same one often
            # as such we use the upstream URL as a unique id
            try:
                exisitng_image = Image.objects.get(
                        upstream_url=image.upstream_url)
            except Image.DoesNotExist:
                logger.debug('INSTAGRAM new image')
                logger.inc_new()
                image.save()
                count +=1
            else:
                logger.debug('INSTAGRAM previously ingested image encountered')
                exisitng_image.date_uploaded = image.date_uploaded
                logger.inc_mod()
                image = exisitng_image
            image.tags.add(*[t[:100] for t in tags])

        max_id = parse_qs(urlsplit(next_).query)['max_tag_id'][0]
