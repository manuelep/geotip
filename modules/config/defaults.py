#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

defaults = {
    # Set DEVELOPMENT to True if this installation is for development
    # or to false if it's for production. When you'll need to distinguish the two
	# situations in your code, for example for logging purposes you can refere to
	# this parameter.
    "DEVELOPMENT": False,
    # Set migrate_anabled and migrate values to False if at the moment of the
    # installation the dedicated database is not empty and the tables described
    # in the model are already defined in the DB engine.
    "migrate": True,
    "migrate_enabled": True,
    # The connection strings to the databases
    "db": 'sqlite://storage.sqlite',
    # "sdb": 'sqlite://scheduler.sqlite',
    # Add here under other variable accordingly to your needs.
	# Values could be any simple type such as string, integer, float or boolean
	# or at leas a dictionary with simple values in it.
}
