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
}


parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)


class BlogPostDetail(Resource):

    @marshal_with(post_fields)
    def get(self, id):
        post = Post.query.filter_by(id=id).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(id))
        return post

    @login_required
    @has_permissions(['blog_can_edit'])
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(id))
        db.session.delete(post)
        db.session.commit()
        return {}, 204

    @marshal_with(post_fields)
    @login_required
    @has_permissions(['blog_can_edit'])
    def put(self, id):
        parsed_args = parser.parse_args()
        post = Post.query.filter_by(id=id).first()
        if not post:
            abort(404, message="Post {} doesn't exist".format(id))
        post.title = parsed_args['title']
        post.content = parsed_args['content']
        db.session.add(post)
        db.session.commit()
        return post, 200


class BlogPostList(Resource):

    @marshal_with(post_fields)
    def get(self):
        post = Post.query.all()
        return post

    @marshal_with(post_fields)
    @login_required
    @has_permissions(['blog_can_post'])
    def post(self):
        parsed_args = parser.parse_args()
        post = Post(title=parsed_args['title'], content=parsed_args['content'])
        db.session.add(post)
        db.session.commit()
        return post, 201


api.add_resource(BlogPostDetail, '/<int:id>')
api.add_resource(BlogPostList, '/')
