# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from piston.handler import AnonymousBaseHandler
import models
import re

class TicketResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        project = 1
        tickets = models.Ticket.objects.filter(project=project)
        out = [{'id': o.id, 'title': o.title} for o in tickets]
        return out

class CommentResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, ticket_id):
        ticket = models.Ticket.objects.get(id=int(ticket_id))
        comments = models.Comment.objects.filter(ticket=ticket)
        out = [{'id': o.id, 'text': o.text} for o in comments]
        return out

class MediaResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, ticket_id):
        pass

class StatusResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        statuses = models.Status.objects.all()
        out = [{'id': o.id, 'title': o.title} for o in statuses]
        return out

