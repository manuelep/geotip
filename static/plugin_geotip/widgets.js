String.format = function() {
	/**
	 * The string containing the format items (e.g. "{key}")
     * will and always has to be the first argument.
	 */
    var theString = arguments[0];

    nfos = arguments[1] || {};
    jQuery.each(nfos, function(key, value){
        var regEx = new RegExp("\\{" + key + "\\}", "gm");
        theString = theString.replace(regEx, value);
    });

    return theString;
}

var zoom_change

function SinglePointEditMap (mapid, map_setup, storeid) {
	/**
	 * a widget for adding and editing just a single point in my geometry field.
       Features are read and stored in the textarea identified by the storeid parameter.

       Options parameters:
	 * mapid 	 @string : div id
	 * map_setup @object : {'center-lat': ..., 'center-lng':..., 'zoom':...}
	 * storeid 	 @string : id of the textarea containing a geojson string
	 */

	var store =  jQuery("#"+storeid);
	var gj = new ol.format.GeoJSON();
	var OSM = new ol.layer.Tile({
		source: new ol.source.OSM(),
		title: 'OpenStreetMap',
		type: 'base',
		visible: true
	});
	var BING = new ol.layer.Tile({
		source: new ol.source.BingMaps({
			key: 'AobLrZ2VLrHz8196Wq9FAqvWL0MrR6slGIfBTWYSUQDN4DR1Vk8F4rXQ4D0Qthlr',
			imagerySet: 'Aerial'
		}),
		title: 'Bing Aerial',
		type: 'base',
		visible: false
	});
	var QUEST = new ol.layer.Tile({
		source: new ol.source.MapQuest({layer: 'hyb'}),
		title: 'MapQuest Satellite',
		type: 'base',
		visible: false
	});
	
	var source = new ol.source.GeoJSON();
	var raw_data = store.text();

	if ( typeof raw_data == 'string' && 
		raw_data!='' && raw_data!='null' &&
	    // test if inputvalue is a valid json string.
	    // courtesy of: https://github.com/douglascrockford/JSON-js/blob/master/json2.js#L464
	    // from: http://stackoverflow.com/questions/3710204/how-to-check-if-a-string-is-a-valid-json-string-in-javascript-without-using-try
	    (/^[\],:{}\s]*$/.test(raw_data.replace(/\\["\\\/bfnrtu]/g, '@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) ) {
	    
		var data = gj.readFeatures(raw_data);
		source.addFeatures(data);

		var geom = data[0].getGeometry();
		var mapcenter = geom.getCoordinates();

	} else {
		// the default center
		var mapcenter = ol.proj.transform(
			[map_setup['center-lng'], map_setup['center-lat']],
			'EPSG:4326', 'EPSG:3857'
		)
	};

	var vector = new ol.layer.Vector({
	  source: source,
	  title: 'Features',
	  style: new ol.style.Style({
	    fill: new ol.style.Fill({
	      color: 'rgba(255, 255, 255, 0.2)'
	    }),
	    stroke: new ol.style.Stroke({
	      color: '#ffcc33',
	      width: 2
	    }),
	    image: new ol.style.Circle({
	      radius: 7,
	      fill: new ol.style.Fill({
	        color: '#ffcc33'
	      })
	    })
	  })
	});

	var map = new ol.Map({
		layers: [
			new ol.layer.Group({
			    'title': 'Base layers',
			    layers: [BING, QUEST, OSM]
			}),
			new ol.layer.Group({
			    'title': 'Overlays',
			    layers: [vector]
			})
        ],
        controls: ol.control.defaults().extend([
            new ol.control.FullScreen()
        ]),
//        renderer: exampleNS.getRendererFromQueryString(),
        target: mapid,
        view: new ol.View({
        	center: mapcenter,
        	zoom: map_setup['zoom']
        })
	});
//	map.addControl(new ol.control.FullScreen())
	var layerSwitcher = new ol.control.LayerSwitcher({
        tipLabel: 'Layers' // Optional label for button
    });
    map.addControl(layerSwitcher);

	var draw; // global so we can remove it later
	function addInteraction() {
	    draw = new ol.interaction.Draw({
	      source: source,
	      type: /** @type {ol.geom.GeometryType} */ ("Point")
	    });
	    draw.on('drawstart', function() {
	    	features = source.getFeatures()
	    	features.slice(0, features.length-1).map(function( feat ){
	    		source.removeFeature(feat);
	    	})
	    	if ( features.length>0 ) {
	    		var text = gj.writeFeaturesObject(features.slice(features.length-1, features.length));
	    		store.text(JSON.stringify(text));
	    	}
	    });
	    map.addInteraction(draw);
	}
	addInteraction();
};

function SinglePointViewMap (mapid, map_setup, storeid) {
	/**
	 * a widget for viewing just a single point in my geometry field.
     *  Features are read from the specified store.
	 *
     * Options parameters:
	 * mapid 	 @string : div id
	 * map_setup @object : {'center-lat': ..., 'center-lng':..., 'zoom':...}
	 * storeid 	 @string : id of the textarea containing a geojson string
	 */

	var raw_data = window[storeid];
	var gj = new ol.format.GeoJSON()
	var OSM = new ol.layer.Tile({
		source: new ol.source.OSM(),
		title: 'OpenStreetMap',
		type: 'base',
		visible: true
	})

	var source = new ol.source.GeoJSON();

	if ( typeof raw_data == 'string' && 
		raw_data!='' && raw_data!='null' &&
	    // test if inputvalue is a valid json string.
	    // courtesy of: https://github.com/douglascrockford/JSON-js/blob/master/json2.js#L464
	    // from: http://stackoverflow.com/questions/3710204/how-to-check-if-a-string-is-a-valid-json-string-in-javascript-without-using-try
	    (/^[\],:{}\s]*$/.test(raw_data.replace(/\\["\\\/bfnrtu]/g, '@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) ) {
	    
		var data = gj.readFeatures(raw_data);
		source.addFeatures(data);

		var geom = data[0].getGeometry();
		var mapcenter = geom.getCoordinates();

	} else {
		// the default center
		var mapcenter = ol.proj.transform(
			[map_setup['center-lng'], map_setup['center-lat']],
			'EPSG:4326', 'EPSG:3857'
		)
	};

	var vector = new ol.layer.Vector({
	  source: source,
	  title: 'Features',
	  style: new ol.style.Style({
	    fill: new ol.style.Fill({
	      color: 'rgba(255, 255, 255, 0.2)'
	    }),
	    stroke: new ol.style.Stroke({
	      color: '#ffcc33',
	      width: 2
	    }),
	    image: new ol.style.Circle({
	      radius: 7,
	      fill: new ol.style.Fill({
	        color: '#ffcc33'
	      })
	    })
	  })
	});
	
	var map = new ol.Map({
		layers: [
			new ol.layer.Group({
			    'title': 'Base layers',
			    layers: [OSM]
			}),
			new ol.layer.Group({
			    'title': 'Overlays',
			    layers: [vector]
			})
        ],
        target: mapid,
        view: new ol.View({
        	center: mapcenter,
        	zoom: map_setup['zoom']
        })
	});
};

function GridMap(mapid, map_setup, storeid) {
	/**
	 * Map to be placed at the top of the grid showing where selected geometries
	 * are placed.
	 * 
	 *  Options parameters:
	 * mapid 	 @string : div id
	 * map_setup @object : {'center-lat': ..., 'center-lng':..., 'zoom':...}
	 * storeid 	 @string : id of the textarea containing a geojson string
	 */

	var raw_data = window[storeid];
	var gj = new ol.format.GeoJSON()
	var OSM = new ol.layer.Tile({
		source: new ol.source.OSM(),
		title: 'OpenStreetMap',
		type: 'base',
		visible: true
	})

	var source = new ol.source.GeoJSON();

	if ( typeof raw_data == 'string' && 
		raw_data!='' && raw_data!='null' &&
	    // test if inputvalue is a valid json string.
	    // courtesy of: https://github.com/douglascrockford/JSON-js/blob/master/json2.js#L464
	    // from: http://stackoverflow.com/questions/3710204/how-to-check-if-a-string-is-a-valid-json-string-in-javascript-without-using-try
	    (/^[\],:{}\s]*$/.test(raw_data.replace(/\\["\\\/bfnrtu]/g, '@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) ) {

		var data = gj.readFeatures(raw_data);
		source.addFeatures(data);

	}

	// the default center
	var mapcenter = ol.proj.transform(
		[map_setup['center-lng'], map_setup['center-lat']],
		'EPSG:4326', 'EPSG:3857'
	);

	var getText = function(feature, resolution, dom) {
		var o = gj.writeFeatureObject(feature);
		if ( o['properties'] ) { return o['properties']['label'] }
		console.log(o)
		return 'Label not defined!'
	};
	
	var createTextStyle = function(feature, resolution, dom) {

		return new ol.style.Text({
			textAlign: 'center',
			textBaseline: 'top',
			font: 'normal 15px Arial',
			text: getText(feature, resolution, dom),
			fill: new ol.style.Fill({color: '#1E90FF'}),
			stroke: new ol.style.Stroke({color: 'white', width: 3}),
//			offsetX: offsetX,
			offsetY: 10,
//			rotation: rotation
		});
	};
	
	var createVectorStyle1 = function() {
		return function(feature, resolution) {
			var style = new ol.style.Style({
				stroke: new ol.style.Stroke({
					color: '#f89406',
					width: 2
				}),
				fill: new ol.style.Fill({
					color: 'rgba(255, 255, 255, 0.2)'
				}),
				image: new ol.style.Circle({
					radius: 7,
					fill: new ol.style.Fill({
						color: '#f89406'
					})
				}),
				text: createTextStyle(feature, resolution)
			});
			return [style];
		};
	};

	var createVectorStyle2 = function() {
		return function(feature, resolution) {
			var style = new ol.style.Style({
				stroke: new ol.style.Stroke({
					color: '#00bfff',
					width: 2
				}),
				fill: new ol.style.Fill({
					color: 'rgba(255, 255, 255, 0.2)'
				}),
				image: new ol.style.Circle({
					radius: 7,
					fill: new ol.style.Fill({
						color: '#00bfff'
					})
				}),
				text: createTextStyle(feature, resolution)
			});
			return [style];
		};
	};

	var vector = new ol.layer.Vector({
		source: source,
		title: 'Features in grid tab',
		style: createVectorStyle1()
	});

	var source2 = new ol.source.GeoJSON();
	var vector2 = new ol.layer.Vector({
	  source: source2,
	  title: 'Features out of grid tab',
	  style: createVectorStyle2()
	});

	
	/**
	 * Add a click handler to the map to render the popup.
	 */
	/**
	 * Elements that make up the popup.
	 */
	var container = document.getElementById('popup');
	var content = document.getElementById('popup-content');
	var closer = document.getElementById('popup-closer');
	/**
	 * Add a click handler to hide the popup.
	 * @return {boolean} Don't follow the href.
	 */
	closer.onclick = function() {
	  overlay.setPosition(undefined);
	  closer.blur();
	  return false;
	};

	/**
	 * Create an overlay to anchor the popup to the map.
	 */
	var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
		element: container,
		autoPan: true,
		autoPanAnimation: {
			duration: 250
		}
	}));
	
	var map = new ol.Map({
		layers: [
			new ol.layer.Group({
			    'title': 'Base layers',
			    layers: [OSM]
			}),
			new ol.layer.Group({
			    'title': 'Overlays',
			    layers: [vector2, vector]
			})
        ],
        overlays: [overlay],
        target: mapid,
        view: new ol.View({
        	center: mapcenter,
        	zoom: map_setup['zoom']
        })
	});

	var layerSwitcher = new ol.control.LayerSwitcher({
        tipLabel: 'Layers' // Optional label for button
    });
    map.addControl(layerSwitcher);

	var the_geom = map_setup['geom-container'];

	function fetch_geoms() {
		extent = map.getView().calculateExtent(map.getSize());
		jQuery.ajax(map_setup['update-url']+'/'+extent.join("/"), {
			success: function (data, status) {
				source2.clear();
				Object.keys(data).map(function (id) {
					var row = data[id];
					feat = gj.readFeatures(JSON.stringify(row[the_geom]));
					source2.addFeatures(feat);
				});
			}
		})
	};
	
	map.getView().on(['change:resolution', 'change:center'], fetch_geoms);
	var extent = source.getExtent();
	map.getView().fitExtent(extent, map.getSize());
	if (map.getView().getZoom() > map_setup['zoom']) {
		map.getView().setZoom(map_setup['zoom']);
	} else {
		fetch_geoms();
	};


	// Popup

	map.on('singleclick', function(evt) {
		// Attempt to find a feature in one of the visible vector layers
	    var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) {
	        return feature;
	    });
	    if (feature) {
	        var coord = feature.getGeometry().getCoordinates();
	        var props = feature.getProperties();
	        content.innerHTML = '<h4>'+props.label+'</h4>'+props.actions;
	        overlay.setPosition(coord);
	    }
	});

	jQuery( ".zoom-to" ).click(function() {
	  center = eval(jQuery( this ).attr('data-zoom-to'));
	  content.innerHTML = '<h4>Here it is!</h4>';
	  overlay.setPosition(center);
	});

};

function MapLoader () {
	/**
	 * The MAP Loader
	 */
	jQuery('.geotipmap').each(function (i) {
		var div = jQuery(this)
		var maptype = eval(div.attr('data-map'));
		var mapid = div.attr('id');
		var map_setup = {
		    'center-lat': eval(div.attr('data-map-center-lat')),
	    	'center-lng': eval(div.attr('data-map-center-lng')),
    		'zoom': eval(div.attr('data-map-zoom')),
    		'update-url': div.attr('data-map-update-url'),
    		'geom-container': div.attr('data-map-geom-field-name'),
		};
		//var storeid = jQuery("#"+div.attr('data-map-source'))
		var storeid = div.attr('data-map-source');
		maptype(mapid, map_setup, storeid);
	});
};

//jQuery( window ).ready( MapLoader() );
//window.onload = MapLoader();