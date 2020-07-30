from app.auth.views import auth


def routes_list():
    routes = [
        {'method': 'POST', 'path': 'register', 'view': auth.login, 'name': 'auth_login'},
        {'method': 'POST', 'path': 'login', 'view': auth.logout, 'name': 'auth_logout'},
    ]

    return routes
