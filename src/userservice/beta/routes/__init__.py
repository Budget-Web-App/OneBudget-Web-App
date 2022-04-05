from beta.routes import signin

def register_routes(app,parent):
    #budgets.register_route(parent)
    #categories.register_route(parent)
    #users.register_route(parent)
    signin.register_route(app, parent)