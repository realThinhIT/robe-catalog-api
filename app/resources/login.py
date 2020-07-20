import jwt
from flask import jsonify
from flask_restful import Resource, request
from werkzeug.security import check_password_hash

from ..models.user import UserModel
from ..schemas.user import UserSchema
from marshmallow import ValidationError
from ..handles.common_handles import BadRequest
from app.config import config


class Login(Resource):
    @staticmethod
    def post():
        """
        Login
        :return: Access token
        """
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = UserModel.find_by_username(username)
        if user and check_password_hash(user.password, password):
          token = jwt.encode({
            'id': user.id
          }, config.SECRET_KEY)

          return jsonify({
              'access_token': token.decode('utf-8')
          })
        else:
          raise BadRequest('Incorrect username or password')
        
