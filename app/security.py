from functools import wraps

import jwt
from werkzeug.security import check_password_hash
from flask import request

from app.config import config
from .models.user import UserModel
from app.handles.common_handles import AuthorizationProblem


def jwt_required():
    """
    Check access token if it's required and then decode it
    :return:
    """
    def decorated(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            access_token = request.headers.get('Authorization')

            print(access_token)
            if access_token is not None:
                try:
                    decoded_data = jwt.decode(
                        access_token.replace('Bearer ', ''), config.SECRET_KEY, algorithms=['HS256'])
                    print(decoded_data)    
                    kwargs['user'] = UserModel.find_by_id(decoded_data['id'])
                except Exception as e:
                    print(e)
                    raise AuthorizationProblem()

            return f(*args, **kwargs)

        return wrapper

    return decorated