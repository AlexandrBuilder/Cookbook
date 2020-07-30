from app.cookbook.views import users, recipes, images, likes, selected_recipes
from app.cookbook.views.admin import users as admin_users, tags as admin_tags, recipes as admin_recipes


def routes_list():
    return [
        {'method': 'POST', 'path': r'/api/user/add', 'view': users.user_add, 'name': 'user_add'},
        {'method': 'GET', 'path': r'/api/user/{username}', 'view': users.user_view, 'name': 'user_view'},
        {'method': 'GET', 'path': r'/api/users', 'view': users.user_list, 'name': 'user_list'},

        {'method': 'POST', 'path': r'/api/recipe/add', 'view': recipes.recipe_add, 'name': 'recipe_add'},
        {'method': 'GET', 'path': r'/api/recipe/{id:\d+}', 'view': recipes.recipe_view, 'name': 'recipe_view'},
        {'method': 'GET', 'path': r'/api/recipes', 'view': recipes.recipe_list, 'name': 'recipe_list'},

        {'method': 'POST', 'path': r'/api/image/add', 'view': images.image_add, 'name': 'image_add'},
        {'method': 'GET', 'path': r'/api/image/{filename}', 'view': images.image_view, 'name': 'image_view'},

        {'method': 'POST', 'path': r'/api/like/add', 'view': likes.like_add, 'name': 'like_add'},

        {'method': 'POST', 'path': r'/api/selected_recipe/add', 'view': selected_recipes.selected_recipe_add,
            'name': 'selected_recipes'},

        {'method': 'POST', 'path': r'/api/admin/user/{username}', 'view': admin_users.user_change_status, 'name':
            'admin_user_change_status'},

        {'method': 'POST', 'path': r'/api/admin/tag/add', 'view': admin_tags.tag_add, 'name': 'admin_tag_add'},

        {'method': 'POST', 'path': r'/api/admin/recipe/{id:\d+}', 'view': admin_recipes.recipe_change_status,
            'name': 'admin_recipe_change_status'},
    ]
