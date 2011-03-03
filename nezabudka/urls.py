# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from piston.resource import Resource
import handlers

urlpatterns = patterns(
    '',
    url(r'^tickets/$', Resource(handler=handlers.TicketResource)),
    url(r'^comments/(?P<ticket_id>\d+)/$', Resource(handler=handlers.CommentResource)),
    url(r'^media/(?P<ticket_id>\d+)/$', Resource(handler=handlers.MediaResource)),
    url(r'^statuses/$', Resource(handler=handlers.StatusResource)),

    url(r'^comments/add/$', Resource(handler=handlers.CommentAddResource)),

    url(r'^$', direct_to_template, {'template': 'nezabudka.html',}, name='index_page'),
)