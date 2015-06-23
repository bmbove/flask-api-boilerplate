from app import db

from flask import Blueprint, g

from flask_restful import Api, Resource 
from flask.ext.restful import abort, fields, marshal_with, reqparse

from app.base.decorators import login_required, has_permissions
from app.blog.models import BlogPost as Post

blog_bp = Blueprint('blog_api', __name__)
api = Api(blog_bp)

post_fields = {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'content': fields.String,
    'slug': fields.String,
}

list_fields = {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'slug': fields.String,
}


parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)


class BlogPostDetail(Resource):

    @marshal_with(post_fields)
    def get(self, slug):
        post = Post.query.filter_by(slug=slug).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(slug))
        return post

    @login_required
    def delete(self, slug):
        post = Post.query.filter_by(slug=slug).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(slug))
        db.session.delete(post)
        db.session.commit()
        return {}, 204

    @marshal_with(post_fields)
    @login_required
    def put(self, slug):
        parsed_args = parser.parse_args()
        post = Post.query.filter_by(slug=slug).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(slug))
        post.title = parsed_args['title']
        post.content = parsed_args['content']
        db.session.add(post)
        db.session.commit()
        return post, 200


class BlogPostList(Resource):

    @marshal_with(list_fields)
    def get(self):
        post = Post.query.all()
        return post

    @marshal_with(post_fields)
    @login_required
    def post(self):
        parsed_args = parser.parse_args()
        title = parsed_args['title']
        content = parsed_args['content']
        if title == '' or content == '':
            abort(400, message="title, content cannot be empty");
        post = Post(title=parsed_args['title'], content=parsed_args['content'])
        db.session.add(post)
        db.session.commit()
        return post, 201


api.add_resource(BlogPostDetail, '/<string:slug>')
api.add_resource(BlogPostList, '/')
