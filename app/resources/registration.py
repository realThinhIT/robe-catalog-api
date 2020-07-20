import jwt
from flask import jsonify
from flask_restful import Resource, request
from ..models.user import UserModel
from ..schemas.user import UserSchema
from marshmallow import ValidationError
from ..handles.common_handles import ServerProblem, BadRequest
from app.config import config


class Registration(Resource):
    """
    Registration resource
    """
    schema = UserSchema()

    @staticmethod
    def post():
        """
        Add new user to the database
        :return: Access token
        """
        data = request.get_json()

        try:
            Registration.schema.load(data)
        except ValidationError as err:
            raise BadRequest(err.messages)
        user = UserModel(**data)
        try:
            user.save_to_db()
        except Exception:
            raise ServerProblem()
        
        token = jwt.encode({
            'id': user.id
        }, config.SECRET_KEY)

        return jsonify({
            'access_token': token.decode('utf-8')
        })
