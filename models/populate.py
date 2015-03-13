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