# /portfolio/models.py

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def get_id(self):
        return str(self.id)




class PortfolioItemDB(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_desc = db.Column(db.String(255), nullable=False)
    long_desc = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    demo_link = db.Column(db.String(255), nullable=True)
    github_link = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<PortfolioItem {self.title}>'

    @classmethod
    def get_all_items(cls):
        return cls.query.all()

    @classmethod
    def get_item_by_id(cls, item_id):
        return cls.query.get(item_id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


from .models import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all():
        return Tag.query.all()

    @staticmethod
    def get_by_id(id):
        return Tag.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create(name):
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return tag

    def edit(self, name):
        self.name = name
        db.session.commit()

class Subtag(db.Model):
    __tablename__ = 'subtags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    tagid = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)
    tag = db.relationship('Tag', backref=db.backref('subtags', lazy=True))

    def __init__(self, name, tagid):
        self.name = name
        self.tagid = tagid

    @staticmethod
    def get_all():
        return Subtag.query.all()

    @staticmethod
    def get_by_id(id):
        return Subtag.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def create(name, tag_id):
        subtag = Subtag(name=name, tag_id=tag_id)
        db.session.add(subtag)
        db.session.commit()
        return subtag

    def edit(self, name, tag_id):
        self.name = name
        self.tag_id = tag_id
        db.session.commit()
