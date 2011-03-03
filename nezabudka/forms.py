# -*- coding: utf-8 -*-
# (c) 2010-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django import forms
from django.shortcuts import get_object_or_404
import models

class CommentAdd(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ('text',)

    # def __init__(self, *args, **kwargs):
    #     super(CommentAdd, self).__init__(*args, **kwargs)
    #     self.base_fields['ticket'].widget = forms.HiddenInput()

    def save(self, user, ticket_id):
        obj = super(CommentAdd, self).save(commit=False)
        obj.user = user
        obj.ticket = get_object_or_404(models.Ticket, pk=ticket_id)
        obj.save()
