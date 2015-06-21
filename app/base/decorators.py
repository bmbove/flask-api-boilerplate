from functools import wraps

from flask import g, request 
from flask.ext.restful import abort

from app.auth.models import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', 'Token Null')
        token = [item.encode('ascii') for item in auth_header.split(' ')]
        if len(token) == 2 and token[0] == 'Token':
            user = User.verify_auth_token(token[1]) 
            if user:
                g.user = user
                return f(*args, **kwargs)
        abort(401, message='Invalid Token - Authorization Required')

    return decorated_function


def has_permissions(perms=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = g.user
            for p in perms:
                if not user.has_permission(p):
                    abort(401, message='Operation not permitted')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
