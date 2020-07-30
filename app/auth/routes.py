from app.auth.views import auth


def routes_list():
    return [
        {'method': 'POST', 'path': r'/api/auth/login', 'view': auth.login, 'name': 'auth_login'},
        {'method': 'POST', 'path': r'/api/auth/logout', 'view': auth.logout, 'name': 'auth_logout'},
    ]
