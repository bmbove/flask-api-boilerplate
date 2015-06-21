from app import app, db
from app.base.models import Base

from passlib.hash import pbkdf2_sha256
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

assoc = db.Table(
    'auth_perm_assoc',
    db.Model.metadata,
    db.Column('auth_user_id', db.Integer, db.ForeignKey('auth_user.id')),
    db.Column('auth_perm_id', db.Integer, db.ForeignKey('auth_perm.id')),
)


class Permission(db.Model):

    __tablename__ = 'auth_perm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    code = db.Column(db.String(128))

    def __init__(self, name, code):
        self.name = name
        self.code = code 

    def __repr__(self):
        return '<Permission %r>' % (self.name)


class User(Base):

    __tablename__ = 'auth_user'

    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    permissions = db.relationship("Permission", secondary=assoc)

    def __init__(self, username, **kwargs):
        self.username = username 
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
        if 'permissions' in kwargs:
            for p in kwargs['permissions']:
                self.add_permission(p)

    def add_permission(self, perm):
        p = Permission.query.filter_by(code=perm).first()
        if p:
            self.permissions.append(p)

    def has_permission(self, perm):
        p = Permission.query.filter_by(code=perm).first()
        if p in self.permissions:
            return True
        else:
            return False

    def check_password(self, password):
        if password is None:
            return False
        return pbkdf2_sha256.verify(password, self.password)

    def set_password(self, password):
        self.password = pbkdf2_sha256.encrypt(password)
        return self.password

    def __repr__(self):
        return '<User %r>' % (self.username)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
