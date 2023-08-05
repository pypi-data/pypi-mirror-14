# -*- coding: utf-8 -*-
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
# from django.views.decorators.cache import never_cache, cache_page
# from django.views.decorators.http import require_http_methods

from .models import MediaStream


def media_stream_detail(request, slug):
    """
    Return a mediastream
    """
    return get_object_or_404(MediaStream, {'slug': slug})
