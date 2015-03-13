# -*- coding: utf-8 -*-

from gluon.custom_import import track_changes; track_changes(True)

import os, logging, logging.handlers
from datetime import datetime, timedelta
from gluon import current
from storage import Storage
from config.config import Config
Config.load()

from plugin_geotip.widgets import PointMapWidget

def get_configured_logger(name):
    """ Courtesy of: http://www.web2pyslices.com/slice/show/1416/logging
    """
    logger = logging.getLogger(name)
    if (len(logger.handlers) == 0):
        # This logger has no handlers, so we can assume it hasn't yet been configured
        # (Configure logger)
        # Create RotatingFileHandler
        # Alternatively we can think to use other handler such as:
        # SQLiteHandler (https://github.com/amka/SQLiteHandler/blob/master/sqlite_handler.py)
        formatter="%(asctime)s %(levelname)s %(process)s %(thread)s %(funcName)s():%(lineno)d %(message)s"
        handler = logging.handlers.RotatingFileHandler(
            os.path.join(request.folder, 'private', request.application+'.log'),
            maxBytes = 1024,
            backupCount = 2
        )
        handler.setFormatter(logging.Formatter(formatter))
        logging_level = logging.DEBUG if current.config.DEVELOPMENT else logging.WARNING
        handler.setLevel(logging_level)
        logger.addHandler(handler)
        logger.setLevel(logging_level)
        
        # Test entry:
        logger.debug(name + ' logger created')
    else:
        # Test entry:
        logger.debug(name + ' already exists')

    return logger

# Assign application logger to a global var  
logger = get_configured_logger(request.application)

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import urllib2
if current.config.db=='postgression':
    if session.postgression is None:
        res = urllib2.urlopen('http://api.postgression.com/')
        session.postgression = Storage(dns=res.read(), time=datetime.now())
    elapsed = datetime.now()-session.postgression.time
    if elapsed > timedelta(minutes=29):
        res = urllib2.urlopen('http://api.postgression.com/')
        session.postgression = Storage(dns=res.read(), time=datetime.now())
    current.config.db = session.postgression.dns

db = DAL(current.config.db, migrate=current.config.migrate, migrate_enabled=current.config.migrate_enabled)

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

from plugin_geotip.widgets import  GeoJsonCollector
    

db.define_table('points',
    Field('name'),
    Field('the_geom', 'json'),
    format = '%(name)s'
)

db.points.the_geom.represent = lambda row: GeoJsonCollector.extract_feature(row, 'the_geom', db.points._format)