# -*- coding: utf-8 -*-

from tasks.models import Task, History, MindMap, UserProfile, Sheet
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


def sync_tasks(request, mmap):
    """
    s
    """
    dec_mmap = zlib.decompress(base64.decodestring(mmap))
    mmap = pickle.loads(dec_mmap)

    now = datetime.datetime.now()
    print "%s: Sync started" % (now)

    # FIXME : fix this! zero level security
    u = UserProfile.objects.get(uuid=mmap['secret'])
    mm, mm_created = MindMap.objects.get_or_create(user=u,
                                                   filename=mmap['file_name'])

    for s in mmap['sheets']:
        sheet, sh_create = Sheet.objects.get_or_create(mind_map=mm,
                                                       title=s['title'])
        for t in s['tasks']:
            path = '/'.join(t['path'])
            task, created = Task.objects.get_or_create(text=t['title'],
                                                       path=path,
                                                       sheet=sheet)

            if created:
                task.text = t['title']
                task.path = path
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
                changed |= set_atribute(task, 'path', path)
                changed |= set_atribute(task, 'color', t['background'] or "FFFFFF")
                changed |= update_progress(task, translate_progress(t['progress']))
                if changed:
                    task.save()
            process_tags(task, t['markers'])
            if 'children' in t:
                process_children(task, t['children'], sheet)

    now2 = datetime.datetime.now()
    print "%s: Sync took %s" % (now2, now2 - now)
