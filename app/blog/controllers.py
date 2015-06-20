from app import db, api
from flask import Blueprint
from flask_restful import Resource

from flask.ext.restful import fields
from flask.ext.restful import marshal_with

from app.blog.models import BlogPost as Post

blog_bp = Blueprint('api', __name__)

todo_fields = {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'content': fields.String,
}

class BlogPost(Resource):

    @marshal_with(todo_fields)
    def get(self, id):
        post = Post.query.filter_by(id=id).first()
        return post

api.add_resource(BlogPost, '/blog/<int:id>')
