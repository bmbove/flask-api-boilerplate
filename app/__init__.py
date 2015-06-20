import flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.restful import abort

app = flask.Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    err = {'message': "Resource doesn't exist."}
    return flask.jsonify(**err)


from app.blog.resources import blog_bp
app.register_blueprint(blog_bp)

db.create_all()

#from app.blog.models import BlogPost as Post
#if True is True:
    #py = Post('Test Post', "Here's some content for this post!")
    #db.session.add(py)
    #db.session.commit()
