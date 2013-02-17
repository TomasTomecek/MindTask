# -*- coding: utf-8 -*-

from tasks.models import Task
#from django.views.decorators.csrf import csrf_exempt
from utils.constants import TASK_MARKERS
from utils.xmlrpc import process_children, process_tags


__all__ = (
    'hello',
    'add_tasks',
    'sync_tasks',
)


def hello(request):
    return "Hello"


def add_tasks(request, tasks):
    for t in tasks:
        task = Task()
        task.text = t['title']
        task.path = '/'.join(t['path'])
        task.color = t['background'] or "FFFFFF"
        task.save()
        process_tags(task, t['markers'])
        if 'children' in t:
            process_children(task, t['children'])


def sync_tasks(request):
    return ""