# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djorm_pgarray.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_ran', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=True)),
                ('info', models.TextField(default=b'', blank=True)),
            ],
            options={
                'ordering': ('-last_ran',),
                'get_latest_by': 'last_ran',
                'verbose_name': 'audit log entry',
                'verbose_name_plural': 'audit log entries',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_identifier', models.CharField(max_length=50, verbose_name='service ID')),
                ('title', models.CharField(help_text='Title or headline of the media.', max_length=255, null=True, verbose_name='title', blank=True)),
                ('description', models.TextField(help_text='Caption or description of what is going on in the media.', null=True, verbose_name='description', blank=True)),
                ('date_taken', models.DateTimeField(help_text='When the media was captured.', verbose_name='date taken')),
                ('longitude', models.DecimalField(null=True, verbose_name='longitude', max_digits=9, decimal_places=6, blank=True)),
                ('latitude', models.DecimalField(null=True, verbose_name='latitude', max_digits=9, decimal_places=6, blank=True)),
                ('visible', models.BooleanField(default=True, help_text='Is this item visible in the stream.', verbose_name='visible')),
                ('user', models.CharField(help_text='Name of the service user who captured the media', max_length=255, verbose_name='user')),
                ('license', models.CharField(help_text='Name of the license', max_length=255, verbose_name='license')),
                ('tags', models.CharField(help_text='Comma-delimited list of tags assigned by the service.', max_length=255, null=True, verbose_name='tags', blank=True)),
                ('media_url', models.URLField(help_text='URL to the original media.', max_length=400, verbose_name='media url')),
                ('media_width', models.PositiveIntegerField(help_text='Width of the original media.', verbose_name='media width')),
                ('media_height', models.PositiveIntegerField(help_text='Height of the original media.', verbose_name='media height')),
                ('media_type', models.CharField(default=b'image/jpeg', max_length=255, verbose_name='media type', choices=[(b'image/jpeg', b'JPEG image'), (b'image/png', b'PNG image'), (b'video/webm', b'WebM Video'), (b'video/mp4', b'MPEG 4 Video')])),
                ('service_url', models.URLField(help_text='URL to the media on the service.', max_length=400, null=True, verbose_name='service url', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date and time this item was added to our database.', verbose_name='date added', auto_now_add=True)),
            ],
            options={
                'ordering': ('-date_taken',),
                'get_latest_by': 'date_taken',
                'verbose_name': 'media',
                'verbose_name_plural': 'media',
            },
        ),
        migrations.CreateModel(
            name='MediaStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('search_terms', models.CharField(help_text='A comma-delimited list of search terms to find media on the selected services.', max_length=255, verbose_name='search terms')),
                ('referesh_rate', models.PositiveIntegerField(default=60, help_text='Number of minutes between refreshes (1 - 1440).', verbose_name='referesh rate', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1440)])),
                ('allowed_media_types', djorm_pgarray.fields.TextArrayField(choices=[(b'image/jpeg', b'JPEG image'), (b'image/png', b'PNG image'), (b'video/webm', b'WebM Video'), (b'video/mp4', b'MPEG 4 Video')], dbtype='text', verbose_name='allowed media types')),
                ('enabled', models.BooleanField(default=True, help_text='When enabled, this stream will aggregate media from the services.', verbose_name='enabled')),
                ('published', models.BooleanField(default=False, help_text='When published, this stream will have its own page on the site.', verbose_name='published')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
            ],
            options={
                'verbose_name': 'Media Stream',
                'verbose_name_plural': 'Media Streams',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('module', models.CharField(max_length=255, verbose_name='module')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
        ),
        migrations.AddField(
            model_name='mediastream',
            name='services',
            field=models.ManyToManyField(related_name='media_streams', to='mediastream.Service'),
        ),
        migrations.AddField(
            model_name='media',
            name='media_stream',
            field=models.ForeignKey(to='mediastream.MediaStream'),
        ),
        migrations.AddField(
            model_name='media',
            name='service',
            field=models.ForeignKey(to='mediastream.Service'),
        ),
        migrations.AddField(
            model_name='auditlogentry',
            name='media_stream',
            field=models.ForeignKey(to='mediastream.MediaStream'),
        ),
        migrations.AddField(
            model_name='auditlogentry',
            name='service',
            field=models.ForeignKey(to='mediastream.Service'),
        ),
        migrations.AlterUniqueTogether(
            name='media',
            unique_together=set([('media_stream', 'service', 'service_identifier')]),
        ),
    ]
