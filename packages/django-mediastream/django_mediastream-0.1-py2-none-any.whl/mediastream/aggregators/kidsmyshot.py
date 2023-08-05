#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
from time import sleep

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from pytz import utc
from requests import get as requests_get

from images.models import Image
from aggregation.models import Source, Log


task_logger = get_task_logger(__name__)
BASE_URL = 'http://kids-myshot.nationalgeographic.com/'
API_PATH = '/api/'


def parse_photo(photo):
    return Image(
            upstream_url=photo['permalink'],
            image_url=photo['large'],
            geolocation=geometry.Point(x=0, y=0, srid=4326),
            title=photo['title'],
            description=photo['description'],
            date_uploaded=utc.localize(datetime.strptime(
                photo['date_uploaded'], '%Y-%m-%dT%H:%M:%S')),
            source=Source.objects.get_or_create(name='Kids My Shot')[0],
            original=photo,
            user=photo['author'],
            ), photo['tags']


@shared_task
def collect():
    log = Log.new(task_logger, 'kidsmyshot', None, False)
    try:
        _collect(log, False)
    except Exception as e:
        log.error('kidsmyshot exception: {}'.format(e))
    log.save_and_cleanup()


@shared_task
def recollect():
    log = Log.new(task_logger, 'kidsmyshot', None, True)
    try:
        _collect(log, True)
    except Exception as e:
        log.error('kidsmyshot exception: {}'.format(e))
    log.save_and_cleanup()


def _collect(logger, recollect=False):
    if not Source.objects.get_or_create(name='Kids My Shot')[0].enabled:
        return

    def col(v):
        return collect_for_tag(logger, v)

    count = sum(map(col, zip(settings.KIDS_MY_SHOT_TAGS,
                             [recollect]*len(settings.KIDS_MY_SHOT_TAGS))))
    logger.info('KIDSMYSHOT {} images ingested'.format(count))

def collect_for_tag(logger, tag_recollect):
    tag, recollect = tag_recollect
    try:
        latest = Image.objects.filter(source__name='Kids My Shot').latest().date_uploaded
    except Image.DoesNotExist:
        latest = settings.AGGREGATION_START_DATE

    params = dict(
            limit=20, # TODO: what's the max?
            tag=tag,
            offset=0,
            )
    count = 0
    err_count = 0
    while True:
        resp = requests_get('{base}{api}{endpoint}'.format(
                api=API_PATH, base=BASE_URL, endpoint='photos.json'),
            params=params.items())
        logger.add_url(resp.request.url)
        if resp.status_code != 200:
            logger.error('KIDSMYSHOT returned {} error'.format(
                resp.status_code))
            return 0

        try:
            resp = resp.json()
        except ValueError:
            logger.warn('KIDSMYSHOT returned invalid JSON')
            sleep(1)
            err_count += 1
            if err_count > 3:
                break
            else:
                continue
        else:
            err_count = 0
        if len(resp['objects']) == 0:
            break
        for photo in resp['objects']:
            image, tags = parse_photo(photo)
            if image.date_uploaded <= latest and not recollect:
                logger.inc_mod()
                return count
            if Image.objects.filter(upstream_url=image.upstream_url).count() > 0:
                logger.inc_mod()
                continue
            logger.inc_new()
            image.save()
            image.tags.add(*tags)

            count +=1
        params['offset'] += len(resp['objects'])

    return count
