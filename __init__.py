from flask import Blueprint
from flask_cors import CORS
from routes.user_routes import user_routes
from routes.category_routes import category_routes
from routes.income_routes import income_routes
from routes.transaction_routes import transaction_routes

main_routes = Blueprint('main_routes', __name__)
CORS(main_routes)

@main_routes.route('/test')
def test():
    return 'test'

main_routes.register_blueprint(user_routes)
main_routes.register_blueprint(category_routes)
main_routes.register_blueprint(income_routes)
main_routes.register_blueprint(transaction_routes)

