# -*- coding: utf-8 -*-

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
