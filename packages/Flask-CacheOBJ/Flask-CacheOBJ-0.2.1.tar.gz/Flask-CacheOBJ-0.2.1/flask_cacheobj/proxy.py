# -*- coding: utf-8 -*-

from flask import current_app
from .consts import __flask_extension_name__

class CacheProxy(object):

    def __getattr__(self, attr):
        if not hasattr(current_app, 'extensions') or \
           __flask_extension_name__ not in current_app.extensions:
            raise Exception('Cache has not been initialized')
        return getattr(current_app.extensions[__flask_extension_name__].mc, attr)

mc = CacheProxy()
