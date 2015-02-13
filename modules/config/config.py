#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon import current
from gluon.contrib import simplejson as json
from storage import Storage
import os.path
from defaults import defaults

indent = 4
this_file_path = os.path.realpath(__file__)

def split_path(p):
    """ Courtesy of: http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
    """
    a,b = os.path.split(p)
    return (split_path(a) if len(a) and len(b) else []) + [b]

config_file_name = 'config.json'
config_path = os.path.join(os.path.join('/', *split_path(this_file_path)[:-3]), 'private', config_file_name)

class Config(object):
    """ """

    @staticmethod
    def read():
        if os.path.isfile(config_path):
            with open(config_path) as config_file:
                o = json.load(config_file)
            return o
        else:
            return {}

    @classmethod
    def load(cls):
        config_update = cls.read()
        current.config = Storage(dict(defaults, **config_update))

    @classmethod
    def write(cls, kw):
        config_diff = cls.read()
        with open(config_path, 'w+') as config_file:
            config_diff.update(dict([(k,v) for k,v in kw.iteritems() if v!=defaults[k]]))
            json.dump(config_diff, config_file, indent=indent)
        cls.load()
