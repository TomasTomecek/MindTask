# -*- coding: utf-8 -*-
"""
functions for retrieval tasks from xmind document

JSON MODEL:
    file_name: file_name,
    sheets: [
        title: sheet_title,
        tasks: [
            {
                'progress': ,
                'markers': ,
                'title': ,
                'path': ,
                'background': ,
                'children': ,
            },
        ]
    ]

"""


import os
from mekk.xmind import XMindDocument
from mekk.xmind.xmlutil import InternalStructureException


__all__ = (
    'get_tasks',
)


TASK_MARKERS = {
    'task-start': 'START',
    'task-quarter': 'QUARTER',
    'task-half': 'HALF',
    'task-3quar': 'ALMOST',
    'task-done': 'DONE',
    'task-pause': 'PAUSE',
}


def find_topic(topic, title):
    """Find topic in node's children"""
    topics = topic.get_subtopics()
    for t in topics:
        if t.get_title() == title:
            return t
    return None


def is_topic_task(topic):
    for marker in topic.get_markers():
        if marker in TASK_MARKERS:
            return marker


def translate_progress(marker):
    return TASK_MARKERS[marker]


def get_children_from_topic(topic, path):
    children = []

    for child in topic.get_subtopics():
        title = child.get_title()
        item = {
            'title': title,
            'path': path,
            'background': topic.get_background_color(),
            'children': get_children_from_topic(child, path + [title]),
        }

        markers = list(topic.get_markers())
        task_marker = is_topic_task(topic)
        if task_marker:
            markers.remove(task_marker)
            item['type'] = 'task'
            item['progress'] = translate_progress(task_marker)
        else:
            item['type'] = 'comment'

        item['markers'] = markers

        children.append(item)

    return children


def get_tasks_from_sheet(sheet, ignore_children=False):
    tasks = []
    options = []
    root = sheet.get_root_topic()

    options.append((root, []))

    while options:
        topic, path = options.pop()
        title = topic.get_title()
        task_marker = is_topic_task(topic)
        if task_marker:
            markers = list(topic.get_markers())
            markers.remove(task_marker)
            task = {
                'progress': translate_progress(task_marker),
                'markers': markers,
                'title': title,
                'path': path,
                'background': topic.get_background_color(),
            }
            if not ignore_children:
                task['children'] = get_children_from_topic(topic,
                                                           path + [title])

            tasks.append(task)
        else:
            options.extend(
                [(t, path + [title]) for t in topic.get_subtopics()]
            )
    return tasks


def get_tasks_from_xdoc(xdoc):
    sheets = []
    for s in xdoc.get_all_sheets():
        sheet = {}
        try:
            sheet['title'] = s.get_title()
        except InternalStructureException:
            s.set_title('Unknown')
            sheet['title'] = "Unknown"
        sheet['tasks'] = get_tasks_from_sheet(s)
        sheets.append(sheet)
    return sheets


def get_tasks(path):
    xmind = XMindDocument.open(path)
    map_tasks = get_tasks_from_xdoc(xmind)
    response = {}
    response['sheets'] = map_tasks
    response['file_name'] = os.path.basename(path)
    return response


if __name__ == '__main__':
    get_tasks("/home/tt/Documents/covscan.xmind")
