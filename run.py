#!/usr/bin/env python
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.config.from_object('config.base')

db = SQLAlchemy(app)
api = Api(app)

if __name__ == '__main__':
    app.run(debug=True)
