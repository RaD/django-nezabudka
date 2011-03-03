# -*- coding: utf-8 -*-
# (c) 2010-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django.conf import settings
from django import get_version
from django.contrib.sites.models import Site

def template_common_vars(request):
    return {
        'settings': settings,
        'user': request.user,
        'django_version': get_version(),
        'site': Site.objects.get_current(),
        'lang_code': request.LANGUAGE_CODE,
        }
