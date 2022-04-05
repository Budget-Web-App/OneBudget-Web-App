from app.mod_api.beta.routes import budgets, categories, users, signin

def register_routes(parent):
    budgets.register_route(parent)
    categories.register_route(parent)
    users.register_route(parent)
    signin.register_route(parent)