# -*- coding: utf-8 -*-

import xmlrpclib
from kobo.xmlrpc import CookieTransport, retry_request_decorator

from xmind import get_tasks

from xmlrpclib import Fault

import zlib
import cPickle as pickle
import base64


def fault_repr(self):
    return "<Fault %s: %s>" % (self.faultCode, str(self.faultString))
Fault.__repr__ = fault_repr


def connect(url):
    TC = retry_request_decorator(CookieTransport)
    tc = TC()

    return xmlrpclib.ServerProxy(url, allow_none=True, transport=tc,
                                 verbose=0)


if __name__ == '__main__':
    xmlrpc_url = "http://127.0.0.1:8000/xmlrpc/client/"

    client = connect(xmlrpc_url)

    path = "/home/tt/Documents/covscan.xmind"

    tasks = get_tasks(path)

    print client.client.hello()

    client.client.sync_tasks(base64.encodestring(zlib.compress(pickle.dumps(tasks))))
