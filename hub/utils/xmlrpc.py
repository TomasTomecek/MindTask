# -*- coding: utf-8 -*-

from tasks.models import Task, Comment, Tag, TagBinding
from utils.constants import TASK_MARKERS

import pdb

__all__ = (
    'process_tags',
    'process_children',
)


def process_tags(model, markers):
    """process tags from JSON, model has to be saved!"""
    for marker in markers:
        if marker in TASK_MARKERS:
            model.progress = TASK_MARKERS.index(marker)
            model.save()
        else:
            obj, created = Tag.objects.get_or_create(name=marker)
            tb = TagBinding(tag=obj, content_object=model)
            tb.save()


def process_children(model, children):
    for item in children:
        if item['type'] == 'task':
            m = Task()
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
