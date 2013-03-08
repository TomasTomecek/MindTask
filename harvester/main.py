#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
Daemon that watches specified path and checks if it has changed. If so, it
pushes data to web-based task manager.
"""

import os
import sys
import time
import ConfigParser

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.events import FileModifiedEvent, FileCreatedEvent, FileMovedEvent

from harvester.hub import sync_file


class EventHandler(FileSystemEventHandler):
    def __init__(self, observer, xmlrpc_url, secret):
        self.observer = observer
        self.xmlrpc_url = xmlrpc_url
        self.secret = secret

    def on_any_event(self, event):
        if isinstance(event, (FileModifiedEvent, FileCreatedEvent,
                              FileMovedEvent)):
            try:
                sync_file(self.xmlrpc_url, event.src_path, self.secret)
            except Exception, e:
                pass
                #print 'Exception while trying to sync data to server', e


def main():
    config = ConfigParser.SafeConfigParser()
    config.read('/etc/harvester.conf')
    path = config.get('General', 'path')
    xmlrpc_url = config.get('General', 'xmlrpc')
    secret = config.get('General', 'secret')

    if not os.path.exists(path):
        return 1

    observer = Observer()
    event_handler = EventHandler(observer, xmlrpc_url, secret)

    observer.schedule(event_handler, path, recursive=os.path.isdir(path))
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    return 0

if __name__ == "__main__":
    sys.exit(main())
