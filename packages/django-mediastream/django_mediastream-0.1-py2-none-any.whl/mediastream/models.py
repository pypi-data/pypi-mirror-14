# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from djorm_pgarray.fields import TextArrayField
from mediastream.settings import MEDIA_TYPE_CHOICES


class ServiceManager(models.Manager):
    _cache = {}

    def get_for_id(self, id):
        """
        Lookup a Service by ID. Uses the same shared cache as get_for_name
        """
        try:
            svc = self.__class__._cache[self.db][id]
        except KeyError:
            # This could raise a DoesNotExist; that's correct behavior and will
            # make sure that only correct ctypes get stored in the cache dict.
            svc = self.get(pk=id)
            self._add_to_cache(self.db, svc)
        return svc

    def get_for_name(self, name):
        """
        Lookup a Service by name. Uses the same shared cache as get_for_id
        """
        try:
            svc = self.__class__._cache[self.db][name]
        except KeyError:
            # This could raise a DoesNotExist; that's correct behavior and will
            # make sure that only correct ctypes get stored in the cache dict.
            svc = self.get(name=name)
            self._add_to_cache(self.db, svc)
        return svc

    def clear_cache(self):
        """
        Clear out the content-type cache. This needs to happen during database
        flushes to prevent caching of "stale" content type IDs (see
        django.contrib.contenttypes.management.update_contenttypes for where
        this gets called).
        """
        self.__class__._cache.clear()

    def _add_to_cache(self, using, svc):
        """Insert a ContentType into the cache."""
        # Note it's possible for ContentType objects to be stale; model_class() will return None.
        # Hence, there is no reliance on model._meta.app_label here, just using the model fields instead.
        key = svc.name
        svc.api = svc.get_api()
        svc.enabled = svc.api is not None
        self.__class__._cache.setdefault(using, {})[key] = svc
        self.__class__._cache.setdefault(using, {})[svc.id] = svc


class Service(models.Model):
    name = models.CharField(_('name'), max_length=50)
    module = models.CharField(_('module'), max_length=255)

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __unicode__(self):
        return self.name

    def get_api(self):
        """
        Load the ServiceAPI module or None
        """
        from django.utils.module_loading import import_string
        from django.core.exceptions import ImproperlyConfigured

        try:
            klass = self.module + '.ServiceAPI'
            return import_string(klass)()
        except (ImportError, ImproperlyConfigured) as e:
            print e
            return None


class MediaStream(models.Model):
    """
    A near-real time aggregation of media from one or more sources based
    on search terms.
    """
    name = models.CharField(
        _('name'),
        max_length=255,
        unique=True)
    slug = models.SlugField(
        _('slug'),
        max_length=255,
        unique=True)
    description = models.TextField(_('description'), blank=True)
    search_terms = models.CharField(
        _('search terms'),
        max_length=255,
        help_text=_('A comma-delimited list of search terms to find media on the selected services.'))
    services = models.ManyToManyField(Service, related_name='media_streams')
    referesh_rate = models.PositiveIntegerField(
        _('referesh rate'),
        default=60,
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        help_text=_('Number of minutes between refreshes (1 - 1440).'))
    allowed_media_types = TextArrayField(
        verbose_name=_('allowed media types'),
        choices=MEDIA_TYPE_CHOICES)
    enabled = models.BooleanField(
        _('enabled'),
        default=True,
        help_text=_('When enabled, this stream will aggregate media from the services.'))
    published = models.BooleanField(
        _('published'),
        default=False,
        help_text=_('When published, this stream will have its own page on the site.'))
    date_created = models.DateTimeField(
        _('date created'),
        auto_now_add=True,
        editable=False)
    date_modified = models.DateTimeField(
        _('date modified'),
        auto_now=True,
        editable=False)

    class Meta:
        verbose_name = _('Media Stream')
        verbose_name_plural = _('Media Streams')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('media_stream_detail', kwargs={'slug': self.slug})


class Media(models.Model):
    """
    A piece of media retrieved from an external source
    """
    media_stream = models.ForeignKey(MediaStream)
    service = models.ForeignKey(Service)
    service_identifier = models.CharField(_('service ID'), max_length=50)
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True, blank=True,
        help_text=_('Title or headline of the media.'))
    description = models.TextField(
        _('description'),
        null=True, blank=True,
        help_text=_('Caption or description of what is going on in the media.'))
    date_taken = models.DateTimeField(
        _('date taken'),
        help_text=_('When the media was captured.'))
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=9,
        decimal_places=6,
        null=True, blank=True)
    latitude = models.DecimalField(
        _('latitude'),
        max_digits=9,
        decimal_places=6,
        null=True, blank=True)
    visible = models.BooleanField(
        _('visible'),
        default=True,
        help_text=_('Is this item visible in the stream.'))
    user = models.CharField(
        _('user'),
        max_length=255,
        help_text=_('Name of the service user who captured the media'))
    license = models.CharField(
        _('license'),
        max_length=255,
        help_text=_('Name of the license'))
    tags = models.CharField(
        _('tags'),
        max_length=255,
        blank=True, null=True,
        help_text=_('Comma-delimited list of tags assigned by the service.'))
    media_url = models.URLField(
        _('media url'),
        max_length=400,
        help_text=_('URL to the original media.'))
    media_width = models.PositiveIntegerField(
        _('media width'),
        help_text=_('Width of the original media.'))
    media_height = models.PositiveIntegerField(
        _('media height'),
        help_text=_('Height of the original media.'))
    media_type = models.CharField(
        _('media type'),
        max_length=255,
        choices=MEDIA_TYPE_CHOICES,
        default=MEDIA_TYPE_CHOICES[0][0])
    service_url = models.URLField(
        _('service url'),
        max_length=400,
        blank=True, null=True,
        help_text=_('URL to the media on the service.'))
    date_added = models.DateTimeField(
        _('date added'),
        auto_now_add=True,
        editable=False,
        help_text=_('The date and time this item was added to our database.'))

    def __unicode__(self):
        return self.title if self.title is not None else '<No Title>'

    class Meta:
        verbose_name = _('media')
        verbose_name_plural = _('media')
        get_latest_by = 'date_taken'
        ordering = ('-date_taken',)
        unique_together = ('media_stream', 'service', 'service_identifier')

    @property
    def is_geolocated(self):
        return self.latitude is not None and self.longitude is not None


class AuditLogEntry(models.Model):
    """
    An indication of what happened the last time a job for a service/media stream ran
    """
    service = models.ForeignKey(Service)
    media_stream = models.ForeignKey(MediaStream)
    last_ran = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    info = models.TextField(default="", blank=True)

    class Meta:
        verbose_name = _('audit log entry')
        verbose_name_plural = ('audit log entries')
        get_latest_by = 'last_ran'
        ordering = ('-last_ran', )
