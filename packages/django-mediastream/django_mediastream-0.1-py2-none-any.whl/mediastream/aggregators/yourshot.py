#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from time import sleep
from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from pytz import utc
from requests import get as requests_get

from images.models import Image
from aggregation.models import Source, Log


task_logger = get_task_logger(__name__)
BASE_URL = 'http://yourshot.nationalgeographic.com'
API_PATH = '/api/v1/'


def parse_photo(photo, source_name):
    return Image(
            upstream_url=BASE_URL + photo['absolute_url'],
            image_url=BASE_URL + photo['sizes']['medium-640'],
            geolocation=geometry.Point(x=float(photo['location']['longitude']) if photo['location']['longitude'] else 0,
                                       y=float(photo['location']['latitude']) if photo['location']['latitude'] else 0,
                                       srid=4326),
            title=photo['title'],
            description=photo['caption'],
            date_uploaded=utc.localize(datetime.strptime(
                photo['publication_date'][:19], '%Y-%m-%dT%H:%M:%S')),
            source=Source.get_by_name(source_name),
            original=photo,
            # WTF the id isn't their id??
            #user_url='http://yourshot.nationalgeographic.com/profile/{}/'.format(
            #    photo['owner']['id']),
            user_url='http://yourshot.nationalgeographic.com/profile/{}/'.format(
                photo['owner']['resource_uri'].rstrip('/').rsplit('/', 1)[-1]),
            user=photo['owner']['display_name']
                    if photo['owner']['display_name'] else 'None',
            ), photo['tags'] + [c['name'] for c in photo['categories']]


@shared_task
def collect(tags, source_name):
    log = Log.new(task_logger, 'yourshot', None, False)
    try:
        _collect(log, tags, source_name, False)
    except Exception as e:
        log.error('yourshot exception: {}'.format(e))
    log.save_and_cleanup()


@shared_task
def recollect(tags, source_name):
    log = Log.new(task_logger, 'yourshot', None, True)
    try:
        _collect(log, tags, source_name, True)
    except Exception as e:
        log.error('yourshot exception: {}'.format(e))
    log.save_and_cleanup()


def _collect(logger, tags, source_name, recollect=False):
    logger.info('YOURSHOT collect started')
    for tag in tags:
        _collect_tag(logger, tag, source_name, recollect)


def _collect_tag(logger, tag, source_name, recollect=False):
    try:
        latest = Image.objects.filter(source__name=source_name).latest().date_uploaded
    except Image.DoesNotExist:
        latest = settings.AGGREGATION_START_DATE
    if recollect:
        latest = settings.AGGREGATION_START_DATE

    params = dict(
            format='json',
            limit=100, # TODO: what's the max?
            order_by='-publication_date',
            publication_date_gte=latest.strftime('%Y-%m-%d'),
            tag=tag,
            offset=0,
            apikey=settings.YOUR_SHOT_KEY,
            )
    count = 0
    while True:
        resp = requests_get('{base}{api}{endpoint}'.format(
                api=API_PATH, base=BASE_URL, endpoint='photo'),
            params=params.items())
        logger.add_url(resp.request.url)
        if resp.status_code != 200:
            logger.error('YOURSHOT returned {} error'.format(
                resp.status_code))
            sleep(1)
            continue

        try:
            resp = resp.json()
        except ValueError:
            logger.warn('YOURSHOT returned invalid JSON')
            continue
        if len(resp['objects']) == 0:
            break
        for photo in resp['objects']:
            image, tags = parse_photo(photo, source_name)
            if image.date_uploaded <= latest:
                logger.info('YOURSHOT {} images ingested'.format(count))
                return
            if Image.objects.filter(upstream_url=image.upstream_url,
                                    source=image.source).count() == 0:
                image.save()
                logger.inc_new()
            else:
                image = Image.objects.get(upstream_url=image.upstream_url,
                                          source=image.source)
                logger.inc_mod()

            image.tags.add(*tags)
            params['offset'] += 1
            count +=1

    logger.info('YOURSHOT {} images ingested'.format(count))
