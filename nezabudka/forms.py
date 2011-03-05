# -*- coding: utf-8 -*-
# (c) 2010-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext, ugettext_lazy as _
import models

class TicketAdd(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ('title', 'component', 'category', 'priority', 'severity', 'assigned_to',)

    def save(self, user, project_id):
        obj = super(TicketAdd, self).save(commit=False)
        obj.user = user
        obj.project = get_object_or_404(models.Project, pk=project_id)
        obj.status = get_object_or_404(models.Status, pk=1)
        obj.save()

class CommentAdd(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ('text',)

    def save(self, user, ticket_id):
        obj = super(CommentAdd, self).save(commit=False)
        obj.user = user
        obj.ticket = get_object_or_404(models.Ticket, pk=ticket_id)
        obj.save()

class Status(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ('status',)

    def save(self, user):
        ticket = super(Status, self).save()

        template = _(u'Status changed: %s.')
        comment = models.Comment(user=user,
                                 ticket=ticket,
                                 text=template % ticket.status)
        comment.save()



