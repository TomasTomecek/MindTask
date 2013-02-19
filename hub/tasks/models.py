from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models import Q

from itertools import chain

from utils.constants import *


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
          return "%s's profile" % self.user

    def __unicode__(self):
        return u"%s" % self.user


class MindMap(models.Model):
    name = models.CharField(max_length=32)
    filename = models.CharField(max_length=128)
    date_created = models.DateTimeField(auto_now_add=True)
    last_synced = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u"#%d %s %s" % (self.id, self.name, self.last_synced)


class Stream(models.Model):
    name = models.CharField(max_length=32)
    color = models.SlugField(max_length=6)


class Component(models.Model):
    name = models.CharField(max_length=64)
    color = models.SlugField(max_length=6)


class Tag(models.Model):
    name = models.CharField(max_length=32)
    color = models.SlugField(max_length=6)


class Entry(models.Model):
    text = models.TextField()
    color = models.SlugField(max_length=6)
    path = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    parent = generic.GenericForeignKey('content_type', 'object_id')

    # http://blog.roseman.org.uk/2010/02/15/django-patterns-part-3-efficient-generic-relations/
    def children(self):
        task_ct = ContentType.objects.get_for_model(Task)
        comment_ct = ContentType.objects.get_for_model(Comment)
        return Entry.objects.filter(
            Q(
                content_type=task_ct,
                object_id=self.id,) |
            Q(
                content_type=comment_ct,
                object_id=self.id,)
        )

    # objects that have instance set as parrent
    tags = generic.GenericRelation('TagBinding')

    def __unicode__(self):
        return u"#%d %s" % (self.id, self.text[:25])


class Task(Entry):

    severity = models.PositiveIntegerField(choices=SEVERITY.get_mapping(),
                                           blank=True, null=True)
    priority = models.PositiveIntegerField(choices=PRIORITY.get_mapping(),
                                           blank=True, null=True)
    progress = models.PositiveIntegerField(choices=PROGRESS.get_mapping(),
                                           blank=True, null=True)
    stream = models.ForeignKey(Stream, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    mmap = models.ForeignKey(MindMap, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_synced = models.DateTimeField(blank=True, null=True)
    component = models.ForeignKey(Component, blank=True, null=True)

    def __unicode__(self):
        return u"[T]#%d %s" % (self.id, self.text[:25])

    def progress_nice_text(self):
        return PROGRESS.get_item_help_text(self.progress)

    def progress_text(self):
        return PROGRESS.get_value(self.progress)


class Comment(Entry):
    def __unicode__(self):
        return u"[C]#%d %s" % (self.id, self.text[:25])


class TagBinding(models.Model):
    tag = models.ForeignKey(Tag)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')




class History(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    action = models.PositiveIntegerField(choices=ACTIONS.get_mapping(),
                                         blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class Remote(models.Model):
    hostname = models.CharField(max_length=64)
    secret = models.CharField(max_length=64)
    user = models.ForeignKey(UserProfile)


class UserSettings(models.Model):
    user = models.ForeignKey(UserProfile)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=64)