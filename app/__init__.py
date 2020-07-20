from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from app.resources.registration import Registration
from app.resources.category_list import CategoryList
from app.resources.category import Category
from app.resources.item import Item
from app.resources.item_list import ItemList
from app.resources.me import Me
from app.resources.login import Login
from app.config import config
from app.handles.common_handles import BadRequest, NotFound, _BaseErrorHandler


def create_app():
    # Create and configure an instance of the Flask application
    from app.db import init_db

    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config)
    api = Api(app)

    # End points definition
    api.add_resource(Registration, '/registrations')
    api.add_resource(CategoryList, '/categories')
    api.add_resource(Category, '/categories/<int:category_id>')
    api.add_resource(ItemList, '/categories/<int:category_id>/items')
    api.add_resource(Item, '/categories/<int:category_id>/items/<int:item_id>')
    api.add_resource(Me, '/me')
    api.add_resource(Login, '/login')
    init_db()

    # Errors handles registration
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            'status_code': 404,
            'message': 'Not found'
        }), 400

    @app.errorhandler(_BaseErrorHandler)
    def handle_error(error):
        print(error)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
