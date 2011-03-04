# -*- coding: utf-8 -*-
# (c) 2010-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from piston.resource import Resource
import handlers

urlpatterns = patterns(
    '',
    url(r'^tickets/$', Resource(handler=handlers.TicketListResource)),
    url(r'^ticket/$', Resource(handler=handlers.TicketResource), name='ticket'),
    url(r'^comments/(?P<ticket_id>\d+)/$', Resource(handler=handlers.CommentResource), name='comments'),
    url(r'^media/(?P<ticket_id>\d+)/$', Resource(handler=handlers.MediaResource)),
    url(r'^statuses/$', Resource(handler=handlers.StatusResource)),


    url(r'^$', direct_to_template, {'template': 'nezabudka.html',}, name='index_page'),
)
