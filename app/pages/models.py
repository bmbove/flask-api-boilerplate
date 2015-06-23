from app import db
from app.base.models import Base

class Page(Base):

    __tablename__ = 'pages_page'

    title = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text(), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title, content, **kwargs):
        self.title = title 
        self.content = content 
        self.set_slug(self.title)

    def __repr__(self):
        return '<Page %r>' % (self.title)
