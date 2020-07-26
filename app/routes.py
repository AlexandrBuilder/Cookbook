from .views import auth, users, recipes, images
from .views.admin import users as admin_users


def setup_routes(app):
    app.router.add_route('POST', '/api/user/add', users.user_add)
    app.router.add_route('GET', '/api/user/{username}', users.user_view)
    app.router.add_route('POST', '/api/recipe/add', recipes.recipes_add)
    app.router.add_route('POST', '/api/user/add', users.user_add)
    app.router.add_route('POST', '/api/image/add', images.images_add)
    app.router.add_route('GET', '/api/image/{filename}', images.images_get)
    app.router.add_route('POST', '/api/auth/login', auth.login)
    app.router.add_route('POST', '/api/auth/logout', auth.logout)
    app.router.add_route('POST', '/api/admin/user/{username}', admin_users.change_status)
