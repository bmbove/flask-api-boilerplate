import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.restful import abort
from flask.ext.migrate import Migrate

app = flask.Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def not_found(error):
    err = {'message': "Resource doesn't exist."}
    return flask.jsonify(**err)


from app.blog.resources import blog_bp
from app.auth.resources import auth_bp

app.register_blueprint(
    blog_bp,
    url_prefix='/blog'
)

app.register_blueprint(
    auth_bp,
    url_prefix='/auth'
)
