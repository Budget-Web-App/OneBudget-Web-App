from app.mod_api.beta.routes import budgets, categories, users

def register_routes(parent):
    budgets.register_route(parent)
    categories.register_route(parent)
    users.register_route(parent)