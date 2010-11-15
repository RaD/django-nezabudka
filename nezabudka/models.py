# -*- coding: utf-8 -*-
# (c) 2010 Ruslan Popov <ruslan.popov@gmail.com>

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class AbstractGUID(models.Model):
    """ Abstract model to usage GUID as PK."""

    # The parameter blank=True allows to use this field with forms,
    # the field will never be empty because of save() method.
    guid = models.CharField(primary_key=True, max_length=32, blank=True)
    user = models.ForeignKey(User, verbose_name=_(u'User'))
    is_active = models.BooleanField(verbose_name=_(u'Is this record active?'), default=True)
    reg_datetime = models.DateTimeField(verbose_name=_(u'Registered'), auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-is_active', '-reg_datetime')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Fill PK with GUID."""
        import uuid
        if not self.guid or self.guid == u'':
            self.guid = uuid.uuid4().get_hex()
        super(AbstractGUID, self).save(*args, **kwargs)

class Project(AbstractGUID):
    """ Project Description. """

    title = models.CharField(verbose_name=_(u'Title'), max_length=64,
                             help_text=_(u'Project Name'))

    class Meta:
        verbose_name = _(u'Project')
        verbose_name_plural = _(u'Projects')

class Component(AbstractGUID):
    """ Component Description. """

    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    title = models.CharField(verbose_name=_(u'Title'), max_length=64,
                             help_text=_(u'Component Name'))

    class Meta:
        verbose_name = _(u'Component')
        verbose_name_plural = _(u'Components')

class Category(AbstractGUID):
    """ Category Description. """
    component = models.ForeignKey(Component, verbose_name=_(u'Component'))
    title = models.CharField(verbose_name=_(u'Title'), max_length=64,
                             help_text=_(u'Category Name'))

    class Meta:
        verbose_name = _(u'Category')
        verbose_name_plural = _(u'Categories')

class Priority(AbstractGUID):
    title = models.CharField(verbose_name=_(u'Title'), max_length=32,
                             help_text=_(u'Priority Title'))

    class Meta:
        verbose_name = _(u'Priority')
        verbose_name_plural = _(u'Priorities')

class Severity(AbstractGUID):
    title = models.CharField(verbose_name=_(u'Title'), max_length=32,
                             help_text=_(u'Severity Title'))

    class Meta:
        verbose_name = _(u'Severity')
        verbose_name_plural = _(u'Severities')

class Status(AbstractGUID):
    title = models.CharField(verbose_name=_(u'Title'), max_length=32,
                             help_text=_(u'Status Title'))

    class Meta:
        verbose_name = _(u'Status')
        verbose_name_plural = _(u'Statuses')

class Ticket(AbstractGUID):
    parent = models.ForeignKey('self', blank=True, null=True, verbose_name=_('Parent'))
    project = models.ForeignKey(Project, verbose_name=_(u'Project'))
    component = models.ForeignKey(Component, verbose_name=_(u'Component'))
    category = models.ForeignKey(Category, verbose_name=_(u'Category'))
    assigned_to = models.ForeignKey(User, verbose_name=_(u'Assigned To'), related_name=u'assigned_to')
    priority = models.ForeignKey(Priority, verbose_name=_(u'Priority'))
    severity = models.ForeignKey(Severity, verbose_name=_(u'Severity'))
    status = models.ForeignKey(Status, verbose_name=_(u'Status'))
    title = models.CharField(verbose_name=_(u'Title'), max_length=256,
                             help_text=_(u'Ticket Title'))
    class Meta:
        verbose_name = _(u'Ticket')
        verbose_name_plural = _(u'Tickets')

    def __init__(self, *args, **kwargs):
        super(Ticket, self).__init__(*args, **kwargs)
        self._meta.get_field('user').verbose_name = _(u'Reported By')

class Comment(AbstractGUID):
    ticket = models.ForeignKey(Ticket, verbose_name=_(u'Ticket'))
    text = models.TextField()

    @property
    def title(self):
        return self.text[:32]

    class Meta:
        verbose_name = _(u'Comment')
        verbose_name_plural = _(u'Comments')
        ordering = ('reg_datetime',)

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        self._meta.get_field('user').verbose_name = _(u'Reported By')

class Media(AbstractGUID):
    ticket = models.ForeignKey(Ticket, verbose_name=_(u'Ticket'))
    title = models.CharField(verbose_name=_(u'Title'), max_length=256,
                             help_text=_(u'Media Title'))
    filename = models.FileField(verbose_name=_(u'File Name'), upload_to=u'files/attachment')

    class Meta:
        verbose_name = _(u'Media')
        verbose_name_plural = _(u'Media')
        ordering = ('reg_datetime',)

    def __init__(self, *args, **kwargs):
        super(Media, self).__init__(*args, **kwargs)
        self._meta.get_field('user').verbose_name = _(u'Reported By')
