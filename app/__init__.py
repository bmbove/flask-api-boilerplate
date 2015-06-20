from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from app.blog.controllers import blog_bp
app.register_blueprint(blog_bp)

db.create_all()

#from app.blog.models import BlogPost as Post
#if True is True:
    #py = Post('Python', "Here's some content for this post!")
    #db.session.add(py)
    #db.session.commit()
