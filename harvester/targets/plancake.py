# -*- coding: utf-8 -*-
"""
This code is heavily inspired by https://bitbucket.org/srid/pyrtm
"""


__all__ = (
    'Plancake',
    'createPlancake',
    'set_log_level',
)


import json
import logging
from hashlib import md5

from copy import copy

from plancake_constants import *

from urllib import urlencode, urlopen


logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Plancake(object):
    """main class"""
    def __init__(self, api_key, api_secret, user_key, api_ver=5):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_ver = api_ver
        self.user_key = user_key
        self.token = ''
        self.token = self.get_token()
        self.run = PlancakeMethods(self)


    def get_token(self):
        params = {}
        params['api_key'] = self.api_key
        params['user_key'] = self.user_key
        response = self.get('getToken', **params)
        token = response['token']
        return token


    def _sign(self, params, method):
        "Sign the parameters with MD5 hash"
        #del params['token']
        pairs = ''.join(['%s%s' % (k, v) for k, v in sortedItems(params)])
        s = method + pairs + self.api_secret
        LOG.debug(s)
        return md5(s.encode('utf-8')).hexdigest()


    def get(self, method, **params):
        "Get the XML response for the passed `params`."
        params['token'] = self.token
        params['api_ver'] = self.api_ver
        params['sig'] = self._sign(copy(params), method)

        data = openURL(SERVICE_URL + method + '/', params).read()

        LOG.debug(data)

        return json.loads(data.decode('utf-8'))


class PlancakeMethods(object):
    """Class for calling API functions"""

    def __init__(self, plancake):
        self.plancake = plancake

    def add_task(self, text):
        params = {}
        params['descr'] = text
        response = self.plancake.get('addTask', **params)
        return response

    def delete_task(self, task_id):
        params = {}
        params['task_id'] = task_id
        response = self.plancake.get('deleteTask', **params)
        return response

    def get_tasks(self, title=''):
        params = {}
        params['search_query'] = title
        response = self.plancake.get('getTasks', **params)
        return response['tasks']

    def delete_all_tasks(self):
        for t in self.get_tasks():
            self.delete_task(t['id'])


def sortedItems(dictionary):
    keys = list(dictionary.keys())
    keys.sort(key=str)
    for key in keys:
        yield key, dictionary[key]


def openURL(url, queryArgs=None):
    if queryArgs:
        url = url + '?' + urlencode(queryArgs)
    LOG.debug("URL %s", url)
    return urlopen(url)


def createPlancake(api_key, api_secret, user_key):
    """supply all the secret"""
    return Plancake(api_key, api_secret, user_key)


def set_log_level(level):
    '''Sets the log level of the logger used by the module.

    >>> import rtm
    >>> import logging
    >>> rtm.set_log_level(logging.INFO)
    '''
    LOG.setLevel(level)


if __name__ == '__main__':
    pass