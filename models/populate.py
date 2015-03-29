# -*- coding: utf-8 -*-

if current.config.DEVELOPMENT:
    guest = auth.get_or_create_user(
        keys = dict(
            email = "guest@guest.eu",
            first_name = "guest",
            last_name = "guest",
            password = db.auth_user.password.validate('guest')[0]
        ),
        update_fields = [],
        login = False
    )

if current.config.DEVELOPMENT and auth.user_id is None:
    auth.login_user(guest)

    if db(db.points.id>0).count()<20:
        from gluon.contrib.populate import populate
        
        def rnd_crd_gen(_):
            from random import uniform
            from json import loads
            jt = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [%(northing)s, %(easting)s]}, "type": "Feature"}]}'
            easting = uniform(4367840., 5736131.)
            northing = uniform(708817., 2282650.)
            return loads(jt % locals())
        
        db.points.the_geom.compute = rnd_crd_gen
        populate(db.points, n=50, default=False, compute=True)
        
