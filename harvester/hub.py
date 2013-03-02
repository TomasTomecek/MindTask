# -*- coding: utf-8 -*-

import xmlrpclib
from kobo.xmlrpc import CookieTransport, retry_request_decorator

from xmind import get_tasks

from xmlrpclib import Fault

import zlib
import cPickle as pickle
import base64


__all__ = (
    'sync_file',
)


def fault_repr(self):
    return "<Fault %s: %s>" % (self.faultCode, str(self.faultString))
Fault.__repr__ = fault_repr


def connect(url):
    TC = retry_request_decorator(CookieTransport)
    tc = TC()

    return xmlrpclib.ServerProxy(url, allow_none=True, transport=tc,
                                 verbose=0)


def sync_file(xmlrpc_url, path):
    client = connect(xmlrpc_url)
    tasks = get_tasks(path)
    client.client.sync_tasks(
        base64.encodestring(
            zlib.compress(
                pickle.dumps(tasks)
            )
        )
    )

if __name__ == '__main__':
    #xmlrpc = "https://mindtask-mtstage.rhcloud.com/xmlrpc/client/"
    xmlrpc = "http://127.0.0.1:8000/xmlrpc/client/"

    client = connect(xmlrpc)

    path = "/home/tt/Documents/maps/personal.xmind"

    tasks = get_tasks(path)
    tasks['secret'] = '762aabc0f678440b96d5f132d55f4b13'

    print client.client.hello()

    client.client.sync_tasks(base64.encodestring(zlib.compress(pickle.dumps(tasks))))
