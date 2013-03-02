# -*- coding: utf-8 -*-

from tasks.models import Task, History
from utils.constants import ACTIONS
from utils.xmlrpc import *

import datetime
import zlib
import cPickle as pickle
import base64


__all__ = (
    'hello',
    'sync_tasks',
)


def hello(request):
    return "Hello"


def sync_tasks(request, tasks):
    dec_tasks = zlib.decompress(base64.decodestring(tasks))
    tasks = pickle.loads(dec_tasks)
    now = datetime.datetime.now()
    print "%s: Sync started" % (now)
    for t in tasks:
        task, created = Task.objects.get_or_create(text=t['title'])

        if created:
            task.text = t['title']
            task.path = '/'.join(t['path'])
            task.color = t['background'] or "FFFFFF"
            task.progress = translate_progress(t['progress'])
            set_default_stream(task)
            task.save()

            h = History()
            h.action = ACTIONS['NEW']
            h.content_object = task
            h.save()
        else:
            changed = False
            changed |= set_atribute(task, 'text', t['title'])
            changed |= set_atribute(task, 'path', '/'.join(t['path']))
            changed |= set_atribute(task, 'color', t['background'] or "FFFFFF")
            changed |= update_progress(task, translate_progress(t['progress']))
            if changed:
                task.save()
        process_tags(task, t['markers'])
        if 'children' in t:
            process_children(task, t['children'])
        print "%s: processed task" % datetime.datetime.now()
    now2 = datetime.datetime.now()
    print "%s: Sync took %s" % (now2, now2 - now)
