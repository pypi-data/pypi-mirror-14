#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from re import compile as rx_compile, VERBOSE
from datetime import datetime, timedelta

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from pytz import utc
from requests import get as requests_get

from images.models import Image
from images.search_indexes import ImageIndex
from images.views.rpc import get_local_source
from aggregation.models import Source, Log



task_logger = get_task_logger(__name__)
API_URL = 'http://www.inaturalist.org/observations/project/{project}.json'
tz_re = rx_compile("""
(?:
    (?P<utc>Z)
    |
    (?P<sign>[+-])
    (?P<hours>\d\d):(?P<minutes>\d\d)
)""", VERBOSE)


class NoPicError(Exception):
    pass


def parse_observation(observation, source_name):
    date = utc.localize(datetime.strptime(observation['created_at'][:19],
                                          '%Y-%m-%dT%H:%M:%S'))
    tz = tz_re.match(observation['created_at'][23:])
    if tz and not tz.group('utc'):
        offset = timedelta(hours=int(tz.group('hours')),
                           minutes=int(tz.group('minutes')))
        if tz.group('sign') == '+':
            offset *= -1
        date += offset

    tags = observation['tag_list']
    # if observation['iconic_taxon_name']:
    #     tags.append(observation['iconic_taxon_name'])
    tags = filter(lambda x: len(x) < 100, tags)

    try:
        image_url=observation['photos'][0]['medium_url'],
    except IndexError:
        raise NoPicError

    return Image(
            upstream_url=observation['uri'],
            image_url=observation['photos'][0]['medium_url'],
            geolocation=geometry.Point(x=float(observation['longitude']) if observation['longitude'] else 0,
                                       y=float(observation['latitude']) if observation['latitude'] else 0,
                                       srid=4326),
            title=observation['species_guess'],
            description=observation['description'],
            date_uploaded=date,
            source=Source.get_by_name(name=source_name),
            source_identifier=observation['id'],
            original=observation,
            user=observation['user_login'],
            ), tags


## need to parameterize this with the setting values!
@shared_task
def collect(project, config, recollect=False):
    log = Log.new(task_logger, project, config, recollect)
    try:
        collect_project(log, project, config, recollect)
    except Exception as e:
        log.error('exception: {}'.format(e))
    log.save_and_cleanup()


def collect_project(logger, project, config, recollect=False):
    # Default API URL params
    params = {
        'per_page': 200,
        'order_by': 'project',
        'order': 'desc',
        'has': 'photos',
        'page': 1
    }
    # The feed setting can have either a string (project) as the key
    # with the value being the GNP source, or the value can be a dict, in
    # which the key is ignored and the dict is used to retreive the
    # api url GNP source and any api params
    if isinstance(config, (str, unicode)):
        source_name = config
        api_url = API_URL.format(project=project)
    elif isinstance(config, (dict, )):
        source_name = config.get('source')
        api_url = config.get('api_url')
        params.update(config.get('params', {}))

    since = settings.AGGREGATION_START_DATE
    if not recollect:
        try:
            latest = Log.objects.filter(project=project).latest('started')
            since = latest.started
        except Log.DoesNotExist as e:
            logger.error('previous log missing, error: {} reusing start date: {}'.format(e, since))

    logger.info('source:"{}"'.format(source_name, ))
    logger.info('project:"{}"'.format(project, ))
    logger.info('params:"{}"'.format(params, ))

    count = 0
    while True:
        params.update(updated_since=since.isoformat())
        logger.info('parameters: {}'.format(params))
        resp = requests_get(api_url, params=params.items())
        logger.add_url(resp.request.url)

        if resp.status_code != 200:
            logger.error('request error status code: {}'.format(resp.status_code))
            return

        try:
            if not len(resp.json()):
                logger.info('no records found')
                break
        except ValueError:
            logger.warn('invalid json data')
            continue
        for observation in resp.json():
            try:
                image, tags = parse_observation(observation, source_name)
            except NoPicError:
                logger.info('no image found in data: "{}"'.format(observation))
                continue
            try:
                # Get the image by identifier and one of two
                # sources. This source may be inat or local, if it was
                # uploaded via GNP. We want to keep the source `local`
                # so we can keep track of which photos were uploaded
                try:
                    # via GNP.
                    ei = Image.objects.get(
                        source__in=[image.source, get_local_source()],
                        source_identifier=image.source_identifier)
                except (Image.DoesNotExist, ):
                    # Try a second time to get the image by source id.
                    try:
                        ei = Image.objects.filter(
                            upstream_url=image.upstream_url)[0]
                    except (IndexError, ):
                        raise Image.DoesNotExist()

                logger.info('updating existing image: {}'.format(ei.source_identifier))
                ei.title = image.title
                ei.description = image.description
                ei.user = image.user
                ei.upstream_url = image.upstream_url
                ei.date_observed = image.date_observed
                ei.save()
                ei.tags.clear()
                ei.tags.add(*tags)
                logger.inc_mod()
                count +=1
                ImageIndex().update_object(ei)
            except (Image.DoesNotExist, ):
                if Image.objects.filter(
                        upstream_url=image.upstream_url,
                        source=image.source,
                        source__name=source_name).count() > 0:
                    image_url = image.image_url
                    source_id = image.source_identifier
                    image = Image.objects.get(upstream_url=image.upstream_url,
                                              source=image.source,
                                              source__name=source_name)
                    image.image_url = image_url
                    image.source_identifier = source_id

                else:
                    logger.info(
                        'creating new image from inat id: {}'.format(
                            image.source_identifier))
                if not image.image_url:
                    logger.info('no image url found')
                    continue
                logger.inc_new()
                image.save()
                image.tags.add(*tags)
                count +=1


        params['page'] += 1

    logger.info('{} images ingested'.format(count))
