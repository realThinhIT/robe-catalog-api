from flask_restful import Resource, request

from app.security import jwt_required
from ..schemas.user import UserSchema


class Me(Resource):
    """
    User Resource
    """
    schema = UserSchema()

    @staticmethod
    @jwt_required()
    def get(user):
        return Me.schema.dump(user)
