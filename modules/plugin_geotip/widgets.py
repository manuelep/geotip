#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon import current

if current.T is None:
    T = lambda v: v
else:
    T = current.T

from sqlhtml import JSONWidget #, StringWidget, SQLFORM
import serializers
from geojson import FeatureCollection
from geojson import loads as gjsloads
from geojson import loads as gjsdumps
from gluon.contrib import simplejson as json
from tools import getUUID

plugin_folder = 'plugin_geotip'

class GeoJsonCollector(object):

    feature_attributes = dict(
#         properties = dict(
#             id = lambda r: r.id,
#             label = '',
#             name = lambda r: 
#         ),
        style = dict(
#             externalGraphic = URL('static', plugin_folder+'/images/my-marker-blue.png'),
            graphicHeight = 25,
            graphicWidth = 21,
            graphicXOffset = -12,
            graphicYOffset = -25,
            labelYOffset = -7,
            fontColor = "#084F72",
            fontWeight = "bold",
            labelOutlineColor = '#d9edf7',
            labelOutlineWidth = 3
        )
    )

    @classmethod
    def extract_feature(cls, row, fieldname='the_geom', table=None, escape=True, cid=None):
        
        if table._format is None:
            format = lambda r: '%(id)s' % r
        elif isinstance(table._format, basestring) and '%' in table._format:
            format = lambda r: table._format % r
        elif callable(table._format):
            format = table._format
        else:
            assert False, "WARNING! It should never happen. Why it happens?"

        ccid = current.request.cid or cid

        def _get_btngrp():
            """
            <div class="btn-group">
              <button class="btn">Left</button>
              <button class="btn">Middle</button>
              <button class="btn">Right</button>
            </div>
            """
            
            def _get_btn(act, label, icon_class):
                url = URL(extension='load', args=(act, table._tablename, row.id, ), user_signature=True)
                onclick = """jQuery('#%(cid)s').empty(); jQuery.web2py.component('%(url)s', '%(cid)s');""" % dict(cid=ccid, url=url)
                return A(I(_class=icon_class), ' ', T(label),
                    _title=T(label),
                    _class='btn',
                    _href='#', #url,
                    _onclick=onclick,
                    cid = ccid
                )

            return DIV(
                _get_btn("view", "View", "icon-zoom-in"),
                _get_btn("edit", "Edit", "icon-pencil"),
#                 _get_btn("delete", "Delete", "icon-trash"),
                _class="btn-group"
            ).xml()

        def _extract():
            el = row[fieldname] # if tablename is None else row[tablename][fieldname]
            if el is None:
                return None
            else:
                feature = el['features'][0]
                feature['properties'] = dict(
                    id = row.id,
                    name = format(row),
                    label = format(row),
                    title = format(row),
                    actions = _get_btngrp().replace('"', '\\"') if escape else _get_btngrp()
                )
                for key,attrs in cls.feature_attributes.iteritems():
                    for attrname, attr in attrs.iteritems():
                        if not key in feature:
                            feature[key] = {}
                        if callable(attr):
                            feature[key][attrname] = attr(row)
                        else:
                            feature[key][attrname] = attr
            return feature

        return _extract()

    @classmethod
    def extract_features(cls, rows, fieldname='the_geom', table=None):
        def _fiter():
            for row in rows:
                feat = cls.extract_feature(row, fieldname, table)
                if not feat is None:
                    yield feat
        return FeatureCollection([f for f in _fiter()])

class PointMapWidget(JSONWidget):
    _class = 'geojson'

    map_defaults = {
       # Roma: lat: 41.9027835, lng: 12.4963655
       '_data-map-center-lat': 41.9027835,
       '_data-map-center-lng': 12.4963655,
       '_data-map-zoom': 8
    }

    @classmethod
    def edit(cls, field, value, **attributes):
        textarea = cls.widget(field, value, _style = "display:none")
        defaults = cls.map_defaults.copy()
        defaults.update(**{
           '_data-map': 'SinglePointEditMap',
           '_data-map-source': textarea.attributes['_id'],
        })
        return DIV(
            DIV(_id=textarea.attributes['_id']+'_map', _class="geotipmap",
                _style="width: 100%",
                **defaults
            ),
            textarea,
        _class="mapcontainer")

    @classmethod
    def view(cls, value, row):

        if value is None:
            return SPAN(I(_class="icon-map-marker icon-white"), _class="badge")

        if 'view' in current.request.args:
            if isinstance(value, basestring):
                encoded = XML(value)
            else:
                encoded = XML(json.dumps(value))

            map_uuid = 'map_%s_uuid' % getUUID()

            script = SCRIPT("""window.%(map_uuid)s = '%(encoded)s'""" % locals(), _type="text/javascript")
            defaults = cls.map_defaults.copy()
            defaults.update(**{
               '_data-map': 'SinglePointViewMap',
               '_data-map-source': map_uuid
            })
            return DIV(
                DIV(_id=getUUID()+'_map', _class="geotipmap",
                    _style="width: 100%",
                    **defaults
                ),
                script,
            _class="mapcontainer")

        else:
            coordinates = value['features'][0]['geometry']['coordinates']
            return SPAN(A(I(' ', _class="icon-map-marker"), _class="zoom-to", _href="#", **{'_data-zoom-to': json.dumps(coordinates)}), _class="badge badge-warning")
            #return SPAN(I(' ', _class="icon-map-marker"), _class="badge badge-warning")

class Mapgrid(object):
    """
    Warning! To be used as part of a component called with LOAD function.
    """

    map_defaults = {
        # Roma: lat: 41.9027835, lng: 12.4963655
        '_data-map-center-lat': 41.9027835,
        '_data-map-center-lng': 12.4963655,
        '_data-map-zoom': 10
    }

    def __init__(self, fieldname="the_geom"):
        self.fieldname = fieldname
        self.uuid = getUUID()

    def __call__(self, query, **vars):
        if current.request.extension=='json':
            return self._get_features(query)
        else:
            return self._get_grid(query, **vars)

    def _get_grid(self, query, *args, **vars):
        """
        warning: at the moment join are not supported
        """

        # Warinig! JSON columns are not sortable!
        if not any([i in current.request.args for i in ('view', 'edit', )]):
            query._db[query.first.tablename][self.fieldname].readable = False
            vars['links'] = [dict(header=self.fieldname, body=lambda row: query._db[query.first.tablename][self.fieldname].represent(row[self.fieldname], row))]

        grid = SQLFORM.grid(query, *args, **vars)
        if not grid.rows is None:
            current.session['geotipflt'] = [r.id for r in grid.rows]
            map_uuid = 'geotipmap_%s' % self.uuid
            features = GeoJsonCollector.extract_features(grid.rows, self.fieldname, query._db[query.first.tablename])
            encoded = XML(features)
            script = SCRIPT("""window.%(map_uuid)s = '%(encoded)s';""" % locals(), _type="text/javascript")
            defaults = self.map_defaults.copy()
            defaults.update(**{
               '_data-map': 'GridMap',
               '_data-map-source': map_uuid,
               '_data-map-update-url': URL(extension='json', args=(current.request.cid, )),
               '_data-map-geom-field-name': self.fieldname,
               '_data-form-name': self.uuid
            })
            popup = DIV(
                A("", _href="#", _id="popup-closer", _class="ol-popup-closer"),
                DIV("", _id="popup-content"),
                _id="popup", _class="ol-popup", _style="width: 170px;"
            )
            mapcontainer = DIV(
                popup,
                DIV(
                    DIV(
                        _id=map_uuid, _class="geotipmap", _style="width: 100%",
                        **defaults
                    ),
                _class="mapcontainer")
            )
            grid.components.insert(0, mapcontainer)
            grid.components.insert(-1, script)

        if current.request.extension=='load':
            current.response.js = "MapLoader();"
        else:
            grid.components.insert(-1, SCRIPT("MapLoader();", _type="text/javascript"))

        return dict(form=grid)

    def _get_features(self, query):
        db = query._db
        if not db._uri.startswith('postgres'):
            return {}
        mapbox = {}
        for n,k in enumerate(('x1', 'y1', 'x2', 'y2', )):
            mapbox[k] = current.request.args(n+1, cast=float, default=0)

        xx = [v for k,v in mapbox.iteritems() if k.startswith('x')]
        yy = [v for k,v in mapbox.iteritems() if k.startswith('y')]

        sqinfo = dict(
            minx = min(xx),
            maxx = max(xx),
            miny = min(yy),
            maxy = max(yy)
        )

        squery = """
            cast(cast((((((the_geom::json->>'features')::json->>0)::json->>'geometry')::json->>'coordinates')::json->0) as text) as double precision) > %(minx)s AND
            cast(cast((((((the_geom::json->>'features')::json->>0)::json->>'geometry')::json->>'coordinates')::json->0) as text) as double precision) < %(maxx)s AND
            cast(cast((((((the_geom::json->>'features')::json->>0)::json->>'geometry')::json->>'coordinates')::json->1) as text) as double precision) > %(miny)s AND
            cast(cast((((((the_geom::json->>'features')::json->>0)::json->>'geometry')::json->>'coordinates')::json->1) as text) as double precision) < %(maxy)s
        """.strip() % sqinfo

        
        if not current.session['geotipflt'] is None:
            myquery = query&squery&~query.first._table.id.belongs(current.session['geotipflt'])
        else:
            myquery = query&squery

        rows = db(myquery).select()

        def _add_info(row):
            row[self.fieldname] = GeoJsonCollector.extract_feature(row, self.fieldname, query._db[query.first.tablename], False, cid=current.request.args(0))
            return row

        return dict(map(lambda row: (row.id, _add_info(row)), rows))
