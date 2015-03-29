# -*- coding: utf-8 -*-

from gluon.contrib import simplejson as json

class Libs(object):
    """ Conditional javascript libraries loading
    usage:
    add under this definition
    Libs.append(URL('static', 'submodules/.../mylib.css/js'), 'mycontroler', 'mycontroler.myfunction')
    """

    @staticmethod
    def append(url, *args):
        """
        args: list of strings representing controllers (and eventually
              their function where the library linked by url has to be loaded).
              Eg: Libs.append(URL(...), 'c1', 'c2.f')
        """
        c = request.controller
        f = request.function
        cf = '.'.join((c, f, ))
        if args:
            if c in args or cf in args:
                response.files.append(url)
        else:
            response.files.append(url)


#                                    ### Load libraries for the ol3 solution ###

#                                                          #### Openlayers3 ####
Libs.append(URL('static', 'submodules/ol3/css/ol.css'))
Libs.append(URL('static', 'submodules/ol3/build/ol.js'))

#                                                    #### ol3-layerswitcher ####
Libs.append(URL('static', 'submodules/ol3-layerswitcher/examples/layerswitcher.css'))
Libs.append(URL('static', 'submodules/ol3-layerswitcher/src/ol3-layerswitcher.css'))
Libs.append(URL('static', 'submodules/ol3-layerswitcher/src/ol3-layerswitcher.js'))

#                                      #### my custom solution based on ol3 ####
Libs.append(URL('static', 'plugin_geotip/overwrites.css'))
Libs.append(URL('static', 'plugin_geotip/widgets.js'))