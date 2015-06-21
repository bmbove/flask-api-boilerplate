from functools import wraps
from flask import g, request, redirect, url_for
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
        abort(401, message='Invalid Token')

    return decorated_function
