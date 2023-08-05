#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from pytz import utc
from requests import get as requests_get
from taggit.models import Tag, TaggedItem

from images.models import Image
from aggregation.models import Source, Log


task_logger = get_task_logger(__name__)
API_URL = 'http://www.projectnoah.org/api/v1/'
_animal_categories = set(['mammal', 'bird', 'invertebrate', 'reptile',
                          'amphibian', 'fish', 'mollusk', 'other', 'pet' ])


def parse_spotting(spotting):
    tags = set(spotting['tags'])
    tags.add(spotting['category'])
    if spotting['category'] in _animal_categories:
        tags.add('animal')
    images = []
    for i, image in enumerate(
            [spotting['images']['primary']] + spotting['images']['secondary']):
        images.append((Image(
                upstream_url='http://www.projectnoah.org/spottings/{}{}'.format(
                    spotting['id'], '#' + str(i) if i != 0 else ''),
                image_url=image,
                geolocation=geometry.Point(x=float(spotting['location'][1]),
                                           y=float(spotting['location'][0]),
                                           srid=4326),
                title=spotting['name'] if spotting['name'] is not None
                                       else 'Unknown spotting',
                description=spotting['description'],
                date_uploaded=utc.localize(datetime.strptime(
                    spotting['submitted_on'], '%Y-%m-%dT%H:%M:%SZ')),
                source=Source.get_by_name('Project Noah'),
                original=spotting,
                user=spotting['author_name'],
                ), tags))
    return images


@shared_task
def collect():
    log = Log.new(task_logger, 'projectnoah', None, False)
    try:
        _collect(log, False)
    except Exception as e:
        log.error('project noah exception: {}'.format(e))
    log.save_and_cleanup()


@shared_task
def recollect():
    log = Log.new(task_logger, 'projectnoah', None, True)
    try:
        _collect(log, recollect=True)
    except Exception as e:
        log.error('project noah exception: {}'.format(e))
    log.save_and_cleanup()


def _collect(logger, recollect=False):
    logger.info('PROJECTNOAH collect started')
    try:
        latest = Image.objects.filter(source__name='Project Noah').latest().date_uploaded
    except Image.DoesNotExist:
        latest = None
    if recollect:
        latest = None

    url = '{base}spottings'.format(base=API_URL)

    params = dict(
        api_key=__name__,
        mission=settings.PROJECT_NOAH_MISSION,
        limit=100,
        )

    count = 0
    images = []
    alltags = []
    while params.get('cursor', True):
        resp = requests_get(url, params=params)
        logger.add_url(resp.request.url)
        if resp.status_code != 200:
            logger.error('PROJECTNOAH returned {} error'.format(
                resp.status_code))
            return
        try:
            resp = resp.json()
        except ValueError:
            logger.warn('PROJECTNOAH returned invalid JSON')
            continue
        params['cursor'] = resp.get('cursor', False)

        for spotting in resp.get('results', []):
            for image, tags in parse_spotting(spotting):
                if latest is not None and image.date_uploaded <= latest:
                    logger.info('PROJECTNOAH {} images ingested'.format(count))
                    return
                if Image.objects.filter(upstream_url=image.upstream_url).count() > 0:
                    logger.inc_mod()
                    continue
                image.save()
                image.tags.add(*tags)
                logger.inc_new()
                count += 1

    logger.info('PROJECTNOAH {} images ingested'.format(count))
