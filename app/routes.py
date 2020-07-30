from app.auth.routes import routes_list as auth_routes
from app.cookbook.routes import routes_list as cookbook_urls

route_modules = [
    {'routes': auth_routes()},
    {'routes': cookbook_urls()},
]


def setup_routes(app):
    for routes in route_modules:
        for route in routes['routes']:
            app.router.add_route(route['method'], route['path'], route['view'], name=route['name'])
