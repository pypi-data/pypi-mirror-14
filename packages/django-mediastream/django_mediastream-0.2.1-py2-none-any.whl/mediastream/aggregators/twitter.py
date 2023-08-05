#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base64 import b64encode
from time import sleep
from json import dumps as json_dumps, loads as json_loads
try:
    import cPickle as pickle
except ImportError:
    import pickle

from celery import shared_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.contrib.gis.geos import geometry

from pytz import utc
from tweepy import API, OAuthHandler, TweepError

from images.models import Image
from aggregation.models import Source, Log


task_logger = get_task_logger(__name__)
auth = OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY,
                      settings.TWITTER_ACCESS_TOKEN_SECRET)
api = API(auth)


def parse_tweet(tweet):
    original = {'id': tweet.id, 'pickle': b64encode(pickle.dumps(tweet))}
    return Image(
            upstream_url='http://twitter.com/{user}/status/{id}'.format(
                user=tweet.user.screen_name, id=tweet.id),
            image_url=tweet.entities['media'][0]['media_url'],
            source=Source.get_by_name('Twitter'),
            description=tweet.text,
            user=tweet.user.screen_name,
            date_uploaded=utc.localize(tweet.created_at),
            geolocation=geometry.Point(x=float(tweet.geo['coordinates'][1]),
                                       y=float(tweet.geo['coordinates'][0]),
                                       srid=4326)
                if tweet.geo and tweet.geo['type'] == 'Point'
                else geometry.Point(x=0, y=0, srid=4326),
            original=original,
            ), [t['text'] for t in tweet.entities['hashtags']]


def _stupid_original(image):
    original = image.original
    for i in range(5): # arbitrary max depth, didn't want while True
        try:
            return original['id']
        except TypeError:
            original = json_loads(original)


@shared_task
def collect():
    logger = Log.new(task_logger, 'twitter', None, False)
    try:
        _collect(logger)
    except Exception as e:
        logger.error('twitter exception: {}'.format(e))
    logger.save_and_cleanup()


def _collect(logger):
    try:
        latest = Image.objects.filter(source__name='Twitter').latest()
        latest_date = latest.date_uploaded
        latest_id = _stupid_original(latest)
    except Image.DoesNotExist:
        latest_date = settings.AGGREGATION_START_DATE
        latest_id = ''

    params = dict(
            result_type='recent',
            q=settings.TWITTER_SEARCH,
            include_entities=True,
            rpp=100,
            since_id=latest_id,
            )
    count = 0
    while True:
        try:
            tweets = api.search(**params)
            logger.add_url(json_dumps(params))
        except TweepError:
            logger.warn('TWITTER internal error')
            sleep(1)
            continue
        if len(tweets) == 0 or (
                len(tweets) == 1 and tweets[0].id == params.get('max_id')):
            logger.info('TWITTER {} images ingested'.format(count))
            return
        for tweet in tweets:
            if 'media' not in tweet.entities:
                continue
            if (hasattr(tweet, 'retweeted_status')
                    and 'media' in tweet.retweeted_status.entities):
                logger.info('TWITTER skipping retweet')
                continue

            image, tags = parse_tweet(tweet)

            try:
                existing_image = Image.objects.get(
                        upstream_url=image.upstream_url,
                        user=image.user)
            except Image.DoesNotExist:
                logger.debug('TWITTER new image')
                logger.inc_new()
                image.save()
                image.tags.add(*tags)
                count +=1
            else:
                logger.debug('TWITTER previously ingested image encountered')
                logger.inc_mod()

        params['max_id'] = tweet.id
    logger.save_and_cleanup()
