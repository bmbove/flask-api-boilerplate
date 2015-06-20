from app import db

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


class BlogPost(Base):

    __tablename__ = 'blog_blogpost'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    published = db.Column(db.Boolean, default=False)

    def __init__(self, title, content, **kwargs):
        self.title = title 
        self.content = content 
        if 'published' in kwargs:
            self.published = kwargs.get('published')

    def __repr__(self):
        return '<BlogPost %r>' % (self.title)
