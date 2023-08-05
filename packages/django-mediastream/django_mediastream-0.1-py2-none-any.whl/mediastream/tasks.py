import datetime

from .models import Media, AuditLogEntry

# On startup of the background processor:
#  - Check that each configured service has correct configurations
#  - Load enabled Streams
#  - For each stream
#     - Schedule a task to call each configured service to search

# Task Call
#  - Need service and stream as params
#  - Call service with search params
#  - Make Media Elements for the results
#  - Make an Audit record with results
#  - Schedule a task to call the service delayed by the refresh rate


def call_service(stream, service):
    """
    Call the service for the stream
    """
    try:
        last_run = stream.auditlogentry_set.filter(service=service, success=True).latest()
    except AuditLogEntry.DoesNotExist:
        last_run = datetime.datetime.now() - datetime.timedelta(days=7)

    terms = [x.strip() for x in stream.search_terms.split(",")]
    api = service.get_api()
    if api is None:
        print "No API"
        return
    results = service.get_api().search(terms, media_types=stream.allowed_media_types, since=last_run)

    for result in results.items:
        Media.objects.get_or_create(
            media_stream=stream,
            service=service,
            service_identifier=result.service_identifier,
            defaults=dict(
                title=result.title[:255],
                description=result.description,
                date_taken=result.date_taken,
                longitude=result.longitude,
                latitude=result.latitude,
                user=result.user,
                license=result.license[:255],
                tags=result.tags[:255],
                media_url=result.media_url,
                media_height=result.media_height,
                media_width=result.media_width,
                media_type=result.media_type,
                service_url=result.service_url
            )
        )

    audit_log_entry = AuditLogEntry.objects.create(
        service=service,
        media_stream=stream,
        success=results.success,
        info=results.message
    )
    return audit_log_entry
