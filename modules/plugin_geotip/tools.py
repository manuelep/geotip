#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import uuid

def getUUID():
    """ Shortcut for uniforming random map naming """
    return str(uuid.uuid1()).split('-')[0]


