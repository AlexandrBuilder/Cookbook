from .views import auth, users
from .views.admin import users as admin_users


def setup_routes(app):
    app.router.add_route('POST', '/api/user/add', users.user_add)
    app.router.add_route('GET', '/api/user/{username}', users.user_view)
    app.router.add_route('GET', '/api/users', users.user_list)
    app.router.add_route('POST', '/api/auth/login', auth.login)
    app.router.add_route('POST', '/api/auth/logout', auth.logout)
    app.router.add_route('POST', '/api/admin/user/{username}', admin_users.change_status)
