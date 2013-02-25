# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType

from tasks.models import *
from utils.constants import *

import pdb

__all__ = (
    'process_tags',
    'process_children',
    'set_atribute',
    'translate_progress',
    'set_default_stream',
    'update_progress',
)


def set_atribute(model, atrib, value, create_history=False):
    old_value = getattr(model, atrib)
    if not old_value == value:
        setattr(model, atrib, value)
        if create_history:
            h = History()
            h.action = ACTIONS['PROGRESS_UPDATE']
            h.content_object = model
            h.key = 'progress'
            h.value = value
            h.save()
        return True
    return False


def translate_progress(task_progress):
    return PROGRESS_TRANSLATION[task_progress]


def set_default_stream(task):
    if task.progress == PROGRESS['COMPLETED']:
        task.stream = Stream.objects.get(name="completed")
    else:
        task.stream = Stream.objects.get(name="active")


def update_progress(task, progress):
    if set_atribute(task, 'progress', progress, True):
        set_default_stream(task)
        return True
    return False


def process_tags(model, markers):
    """process tags from JSON, model has to be saved!"""
    if not markers:
        return
    # obj, created
    tags = [ Tag.objects.get_or_create(name=marker) for marker in markers ]
    db_tags = TagBinding.objects.filter(
        content_type__pk=ContentType.objects.get_for_model(model).id,
        object_id=model.id,
    )
    # remove all tags that are not associated with model anymore
    db_tags.exclude(tag__in=[tag[0] for tag in tags]).delete()

    db_tags = TagBinding.objects.filter(
        tag__in=[tag[0] for tag in tags]
    )

    for tag, created in tags:
        if not created:
            found = False
            for db_tag in db_tags:
                if db_tag.tag == tag:
                    found = True
                    break
            if found:
                continue
        tb = TagBinding(tag=tag, content_object=model)
        tb.save()


def process_children(model, children):
    db_children = model.children()
    for item in children:
        if db_children.filter(text=item['title']):
            continue
        if item['type'] == 'task':
            m = Task()
            m.progress = translate_progress(item['progress'])
            set_default_stream(m)
        elif item['type'] == 'comment':
            m = Comment()
        else:
            RuntimeError("Invalid item's type %s!" % item['type'])
        #pdb.set_trace()
        m.parent = model
        m.text = item['title']
        m.path = '/'.join(item['path'])
        m.color = item['background'] or "FFFFFF"
        m.save()
        process_tags(m, item['markers'])

        if 'children' in item and item['children']:
            process_children(m, item['children'])
