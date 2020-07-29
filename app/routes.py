from .views import auth, users, recipes, images
from .views.admin import users as admin_users, tags


def setup_routes(app):
    app.router.add_route('POST', r'/api/user/add', users.user_add)
    app.router.add_route('GET', r'/api/user/{username}', users.user_view)
    app.router.add_route('GET', r'/api/users', users.user_list)

    app.router.add_route('POST', r'/api/recipe/add', recipes.recipe_add)
    app.router.add_route('GET', r'/api/recipe/{id:\d+}', recipes.recipe_view)
    app.router.add_route('GET', r'/api/recipes', recipes.recipe_list)

    app.router.add_route('POST', r'/api/image/add', images.image_add)
    app.router.add_route('GET', r'/api/image/{filename}', images.image_view)

    app.router.add_route('POST', r'/api/auth/login', auth.login)
    app.router.add_route('POST', r'/api/auth/logout', auth.logout)

    app.router.add_route('POST', r'/api/admin/user/{username}', admin_users.change_status)

    app.router.add_route('POST', r'/api/admin/tag/add', tags.tag_add)
