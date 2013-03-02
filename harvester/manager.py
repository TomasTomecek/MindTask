# -*- coding: utf-8 -*-
"""
DEPRECATED
Uses plancake API
"""

from targets.plancake import createPlancake

from xmind import get_tasks


P = createPlancake()

def sync_work_dir():

    path = "/home/tt/Documents/covscan.xmind"

    tasks = get_tasks(path)
    for t in tasks:
        P.run.add_task(t['title'])


def delete_all_tasks():
    P.run.delete_all_tasks()

if __name__ == '__main__':
    delete_all_tasks()
    #sync_work_dir()
