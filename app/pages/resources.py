from app import db

from flask import Blueprint, g

from flask_restful import Api, Resource 
from flask.ext.restful import abort, fields, marshal_with, reqparse

from app.base.decorators import login_required, has_permissions
from app.pages.models import Page

page_bp = Blueprint('page_api', __name__)
api = Api(page_bp)

page_fields = {
    'id': fields.Integer,
    'created': fields.DateTime,
    'modified': fields.DateTime,
    'title': fields.String,
    'content': fields.String,
    'slug': fields.String,
}

list_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'slug': fields.String,
}


parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('content', type=str)


class PageDetail(Resource):

    @marshal_with(page_fields)
    def get(self, slug):
        page = Page.query.filter_by(slug=slug).first()
        if not page:
            abort(404, message="Page {} doesn't exist".format(slug))
        return page 

    @login_required
    def delete(self, slug):
        page = Page.query.filter_by(slug=slug).first()
        if not page:
            abort(404, message="Page {} doesn't exist".format(slug))
        db.session.delete(page)
        db.session.commit()
        return {}, 204

    @marshal_with(page_fields)
    @login_required
    def put(self, slug):
        parsed_args = parser.parse_args()
        page = Page.query.filter_by(slug=slug).first()
        if not page:
            abort(404, message="Page {} doesn't exist".format(slug))
        page.title = parsed_args['title']
        page.content = parsed_args['content']
        db.session.add(page)
        db.session.commit()
        return page, 200


class PageList(Resource):

    @marshal_with(list_fields)
    def get(self):
        pages = Page.query.all()
        return pages

    @marshal_with(page_fields)
    @login_required
    def post(self):
        parsed_args = parser.parse_args()
        title = parsed_args['title']
        content = parsed_args['content']
        if title == '' or content == '':
            abort(400, message="title, content cannot be empty");
        page = Page(title=parsed_args['title'], content=parsed_args['content'])
        db.session.add(page)
        db.session.commit()
        return page, 201


api.add_resource(PageDetail, '/<string:slug>')
api.add_resource(PageList, '/')
