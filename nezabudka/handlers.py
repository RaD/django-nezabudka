# -*- coding: utf-8 -*-
# (c) 2010-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.core import exceptions
from piston.handler import AnonymousBaseHandler
from piston.utils import rc, throttle, FormValidationError
from.piston.decorator import decorator as piston_decorator
import models, forms
import re

def validate(v_form, operation='POST'):
    @piston_decorator
    def wrap(f, self, request, *a, **kwa):
        model_instance = None

        if operation == 'PUT':
            if not self.has_model():
                return rc.NOT_IMPLEMENTED

            if 'pk_field' not in kwa: # No pk was specified
                return rc.BAD_REQUEST

            try:
                instance = self.queryset(request).get(pk=kwa.get('pk_field'))
            except exceptions.ObjectDoesNotExist:
                return rc.NOT_FOUND
            except exceptions.MultipleObjectsReturned:
                return rc.BAD_REQUEST

        form = v_form(getattr(request, operation), instance=instance)

        if form.is_valid():
            setattr(request, 'form', form)
            return f(self, request, *a, **kwa)
        else:
            raise FormValidationError(form)
    return wrap

class TicketListResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)
    model = models.Ticket

    project_id = 1

    def read(self, request):
        tickets = self.model.objects.filter(project=self.project_id)
        out = [{'id': o.id, 'title': o.title} for o in tickets]
        return out

class TicketResource(AnonymousBaseHandler):
    allowed_methods = ('GET', 'POST',)
    model = models.Ticket
    fields = ('title', 'component', 'category', 'priority', 'severity', 'assigned_to',)

    project_id = 1

    def read(self, request):
        out = {'form': forms.TicketAdd(initial={'project': self.project_id,}),
               'action': reverse('nezabudka:ticket'),}
        return out

    @throttle(2, 60) # allow 2 times in 1 minutes
    @validate(forms.TicketAdd)
    def create(self, request):
        if hasattr(request, 'form'):
            request.form.save(request.user, self.project_id)
            return rc.ALL_OK

class CommentResource(AnonymousBaseHandler):
    allowed_methods = ('GET', 'POST',)
    model = models.Comment
    fields = ('text',)

    def read(self, request, ticket_id):
        out = {'form': forms.CommentAdd(initial={'ticket': ticket_id,}),
               'action': reverse('nezabudka:comments', kwargs={'ticket_id': int(ticket_id),}),}
        ticket = get_object_or_404(models.Ticket, id=int(ticket_id))
        out['ticket'] = {'id': ticket.id,
                         'title': ticket.title,
                         'assigned_to_id': ticket.assigned_to.id,
                         'assigned_to_username': ticket.assigned_to.username,
                         'status_id': ticket.status.id,
                         'status_title': ticket.status.title,
                         'component_id': ticket.component.id,
                         'component_title': ticket.component.title,
                         'priority_id': ticket.priority.id,
                         'priority_title': ticket.priority.title,
                         'severity_id': ticket.severity.id,
                         'severity_title': ticket.severity.title,
                         }
        comments = self.model.objects.filter(ticket=ticket)
        out['comments'] = [{'id': o.id, 'text': o.text, 'user': o.user.username,
                            'date': o.reg_datetime} for o in comments]
        return out

    @throttle(5, 60) # allow 5 times in 1 minutes
    @validate(forms.CommentAdd, 'POST')
    def create(self, request, ticket_id):
        if hasattr(request, 'form'):
            request.form.save(request.user, ticket_id)
            return rc.ALL_OK

class StatusesResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        statuses = models.Status.objects.all()
        out = [{'id': o.id, 'title': o.title} for o in statuses]
        return out

class StatusResource(AnonymousBaseHandler):
    allowed_methods = ('GET', 'PUT',)
    model = models.Ticket

    def read(self, request, pk_field):
        out = {'form': forms.Status(initial={'ticket': pk_field,}),
               'action': reverse('nezabudka:status', kwargs={'pk_field': int(pk_field),}),}
        return out

    @throttle(5, 60) # allow 5 times in 1 minutes
    @validate(forms.Status, 'PUT')
    def update(self, request, *args, **kwargs):
        if hasattr(request, 'form'):
            request.form.save(request.user)
            return rc.ALL_OK

class MediaResource(AnonymousBaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, ticket_id):
        pass

