# -*- coding: utf-8 -*-
# (c) 2010-2011 Ruslan Popov <ruslan.popov@gmail.com>

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms

from nezabudka import models

class Abstract(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

class m_Project(Abstract):

    list_display = ('title', 'user', 'is_active', 'reg_datetime')
    list_filter = ('user',)
    fieldsets = (
        (None, {'fields': ('title', 'is_active')}),
        )

admin.site.register(models.Project, m_Project)
models.Project.model_desc = _(u'This model consists of projects list.')

class m_Component(Abstract):

    list_display = ('title', 'user', 'project', 'is_active', 'reg_datetime')
    list_filter = ('user', 'project',)
    fieldsets = (
        (None, {'fields': ('project', 'title', 'is_active')}),
        )

admin.site.register(models.Component, m_Component)
models.Component.model_desc = _(u'This model consists of components list.')

class m_Category(Abstract):

    list_display = ('title', 'user', 'component', 'is_active', 'reg_datetime')
    list_filter = ('user', 'component',)
    fieldsets = (
        (None, {'fields': ('component', 'title', 'is_active')}),
        )

admin.site.register(models.Category, m_Category)
models.Category.model_desc = _(u'This model consists of categories list.')

class m_Priority(Abstract):

    list_display = ('title', 'user', 'is_active', 'reg_datetime')
    list_filter = ('user',)
    fieldsets = (
        (None, {'fields': ('title', 'is_active')}),
        )

admin.site.register(models.Priority, m_Priority)
models.Priority.model_desc = _(u'This model consists of priorities list.')

class m_Severity(Abstract):

    list_display = ('title', 'user', 'is_active', 'reg_datetime')
    list_filter = ('user',)
    fieldsets = (
        (None, {'fields': ('title', 'is_active')}),
        )

admin.site.register(models.Severity, m_Severity)
models.Severity.model_desc = _(u'This model consists of severities list.')

class m_Status(Abstract):

    list_display = ('title', 'user', 'is_active', 'reg_datetime')
    list_filter = ('user',)
    fieldsets = (
        (None, {'fields': ('title', 'is_active')}),
        )

admin.site.register(models.Status, m_Status)
models.Status.model_desc = _(u'This model consists of statuses list.')

class MediaInline(admin.StackedInline):
    model = models.Media
    extra = 1
    exclude = ('user', 'is_active',)

class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 1
    exclude = ('user', 'is_active',)

class m_Ticket(Abstract):

    inlines = (MediaInline, CommentInline,)

    list_display = ('title', 'status', 'replies', 'product',
                    'assigned_to', 'priority', 'severity',
                    'user', 'is_active', 'reg_datetime')
    list_filter = ('assigned_to', 'priority', 'severity', 'status',
                   'project', 'component', 'category', 'user',)
    list_editable = ('priority', 'severity', 'status', 'assigned_to')
    fieldsets = (
        (u'Product',
         {'fields': (('project', 'component', 'category'),)}),
        (u'State',
         {'fields': (('priority', 'severity', 'status'),)}),
        (u'Ticket',
         {'fields': ('parent', 'assigned_to', 'title', 'is_active')}),
        )

    def product(self, ticket):
        msg =  _(u'Project: <b>%(project)s</b><br/>Component: <b>%(component)s</b><br/>Category: <b>%(category)s</b>')
        values = { 'project': ticket.project, 'component': ticket.component, 'category': ticket.category }
        return msg % values
    product.short_description = _(u'Product')
    product.allow_tags = True

    def replies(self, ticket):
        return ticket.comment_set.all().count()
    replies.short_description = _(u'Replies')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk: # new record
                instance.user = request.user
            instance.save()
        formset.save_m2m()

admin.site.register(models.Ticket, m_Ticket)
models.Ticket.model_desc = _(u'This model consists of tickets list.')

class m_Comment(Abstract):

    list_display = ('title', 'user', 'ticket', 'is_active', 'reg_datetime')
    list_filter = ('user', 'ticket')
    fieldsets = (
        (None, {'fields': ('ticket', 'text', 'is_active')}),
        )

# hide this model in administrative interface
admin.site.register(models.Comment, m_Comment)
models.Comment.model_desc = _(u'This model consists of comments list.')

class m_Media(Abstract):

    list_display = ('title', 'user', 'ticket', 'is_active', 'reg_datetime')
    list_filter = ('user', 'ticket')
    fieldsets = (
        (None, {'fields': ('ticket', 'title', 'filename', 'is_active')}),
        )

admin.site.register(models.Media, m_Media)
models.Media.model_desc = _(u'This model consists of media list.')
