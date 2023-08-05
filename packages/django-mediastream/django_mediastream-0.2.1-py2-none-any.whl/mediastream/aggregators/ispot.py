#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from json import loads as json_loads
from urllib import urlencode

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from oauth2 import Client, Consumer
from pytz import utc
from taggit.models import Tag, TaggedItem

from images.models import Image
from aggregation.models import Source, Log


task_logger = get_task_logger(__name__)
API_URL = 'http://www.ispot.org.{}/api/observation.json'
DEFAULT_PARAMS = {'page': 1, 'count': 100}


clients = {}
for cctld in ['uk', 'za']:
    key = getattr(settings, 'ISPOT_CONSUMER_KEY_' + cctld.upper())
    secret = getattr(settings, 'ISPOT_CONSUMER_SECRET_' + cctld.upper())
    consumer = Consumer(key=key, secret=secret)
    clients[cctld] = Client(consumer)
_animal_groups = set(['Amphibians and Reptiles', 'Birds', 'Invertebrates'])


def parse_observation(observation, cctld):
    tags = [observation['ispot_group']]
    if observation['ispot_group'] in _animal_groups:
        tags += ['animal']
    user = observation['observer']
    try:
        user = user['username']
    except TypeError:
        pass
    return Image(
            upstream_url='http://www.ispot.org.{}/node/{}'.format(
                cctld, observation['id']),
            image_url='http://www.ispot.org.{}'.format(cctld) + \
                    observation['thumbnail'].replace('/imagecache/thumbnail', ''),
            geolocation=geometry.Point(x=float(observation['location']['coordinates'][0][1]),
                                       y=float(observation['location']['coordinates'][0][0]),
                                       srid=4326),
            title=observation['title'],
            description='',
            date_uploaded=utc.localize(datetime.fromtimestamp(int(
                observation['observed_date']))),
            source=Source.objects.get_or_create(name='iSpot')[0],
            original=observation,
            user=user,
            ), tags

@shared_task
def collect():
    try:
        latest = Image.objects.filter(source__name='iSpot').latest().date_uploaded
    except Image.DoesNotExist:
        latest = settings.AGGREGATION_START_DATE

    log = Log.new(task_logger, 'ispot-uk', None, False)
    try:
        _collect(log, 'uk', latest)
    except Exception as e:
        log.error('ispot exception: {}'.format(e))
    log.save_and_cleanup()

    log = Log.new(task_logger, 'ispot-za', None, False)
    try:
        _collect(log, 'za', latest)
    except Exception as e:
        log.error('ispot exception: {}'.format(e))
    log.save_and_cleanup()


def _collect(logger, cctld, latest):
    params = DEFAULT_PARAMS.copy()
    params['tagids'] = '+'.join(settings.ISPOT_TAGS[cctld])
    params['added_date_from'] = latest.strftime('%m/%d/%Y')

    count = 0
    images = []
    alltags = []
    while True:
        resp, content = clients[cctld].request('{}?{}'.format(
            API_URL.format(cctld), urlencode(params)))
        logger.add_url(API_URL.format(cctld))
        if resp['status'] != '200':
            logger.error('ISPOT {} returned {} error'.format(
                cctld, resp['status']))
            return
        try:
            content = json_loads(content)
        except ValueError:
            logger.warn('ISPOT {} returned invalid JSON'.format(cctld))
            continue

        if len(content['observations']) == 0:
            logger.info('ISPOT {} images ingested'.format(count))
            return

        for observation in content['observations']:
            image, tags = parse_observation(observation, cctld)
            if Image.objects.filter(upstream_url=image.upstream_url).count() > 0:
                logger.inc_mod()
                continue
            image.save()
            image.tags.add(*tags)
            logger.inc_new()
            count += 1
        params['page'] +=1

    logger.info('ISPOT {} images ingested'.format(count))
