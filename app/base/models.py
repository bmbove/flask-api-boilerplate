import re
from unicodedata import normalize

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

    def set_slug(self, text):
        slug = self.slugify(text)
        i = 0
        # hopefully ensure slug is unique
        while self.query.filter_by(slug=slug).count() > 0:
            slug = self.slugify("%s %d" % (text, i))
            i += 1
        self.slug = slug

    @staticmethod
    def slugify(text, delim=u'-'):
        _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        text = unicode(text)
        """Generates an slightly worse ASCII-only slug."""
        result = []
        for word in _punct_re.split(text.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delim.join(result))
