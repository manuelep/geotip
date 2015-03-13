# -*- coding: utf-8 -*-
    
from plugin_geotip.widgets import Mapgrid

def _index():
    db.points.the_geom.widget=PointMapWidget.edit
    db.points.the_geom.represent=PointMapWidget.view
    return Mapgrid()(db.points.id>0, csv=False, paginate=5)

def index():
    form = LOAD(request.controller, '_index.load', ajax=True)
    return locals()