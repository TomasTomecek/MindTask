# -*- coding: utf-8 -*-
"""functions for retrieval tasks from xmind document"""

from mekk.xmind import XMindDocument

__all__ = (
    'get_tasks',
)

TASK_MARKERS = ('task-start', 'task-quarter', 'task-half', 'task-3quar',
                'task-done', 'task-pause',)


def find_topic(topic, title):
    topics = topic.get_subtopics()
    for t in topics:
        if t.get_title() == title:
            return t
    return None

def is_topic_task(topic):
    for marker in topic.get_markers():
        if marker in TASK_MARKERS:
            return marker

def get_children_from_topic(topic, path):
    children = []

    for child in topic.get_subtopics():
        title = child.get_title()

        item = {
            'markers': list(topic.get_markers()),
            'title': title,
            'path': path,
            'background': topic.get_background_color(),
            'children': get_children_from_topic(child, path + [title]),
        }

        if is_topic_task(topic):
            item['type'] = 'task'
        else:
            item['type'] = 'comment'

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
        if is_topic_task(topic):

            task = {
                'markers': list(topic.get_markers()),
                'title': title,
                'path': path,
                'background': topic.get_background_color(),
            }
            if not ignore_children:
                task['children'] = get_children_from_topic(topic, path + [title])

            tasks.append(task)
        else:
            options.extend(
                [(t, path + [title]) for t in topic.get_subtopics()]
            )
    return tasks


def get_tasks_from_xdoc(xdoc):
    tasks = []
    for sheet in xdoc.get_all_sheets():
        tasks.extend(get_tasks_from_sheet(sheet))
    return tasks


def get_tasks(path):
    xmind = XMindDocument.open(path)
    return get_tasks_from_xdoc(xmind)


if __name__ == '__main__':
    get_tasks("/home/tt/Documents/covscan.xmind")