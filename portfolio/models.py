# /portfolio/models.py

from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def get_id(self):
        return str(self.id)



# Define the intermediary table for the many-to-many relationship between PortfolioItemDB and TagDB
tags_to_items = db.Table('tags_to_items',
    db.Column('tagid', db.Integer, db.ForeignKey('tags.id')),
    db.Column('itemid', db.Integer, db.ForeignKey('items.id'))
)

# Define the intermediary table for the many-to-many relationship between PortfolioItemDB and SubTagDB
subtags_to_items = db.Table('subtags_to_items',
    db.Column('subtagid', db.Integer, db.ForeignKey('subtags.id')),
    db.Column('itemid', db.Integer, db.ForeignKey('items.id'))
)


from .models import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Tag {self.name}>'

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
    tag = relationship("Tag", backref="subtags")

    def __repr__(self):
        return f"<Subtag {self.name}>"

    def __repr__(self):
        return f'<SubTag {self.name}>'

    @staticmethod
    def get_by_id(id):
        return Subtag.query.filter_by(id=id).first()

    def create_subtag(self):

        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def update_subtag(subtag_id, name):
        subtag = Subtag.query.filter_by(id=subtag_id).first()
        if subtag:
            subtag.name = name
            db.session.commit()
            return subtag
        return None


    def delete_subtag(self):
        if self:
            db.session.delete(self)
            db.session.commit()
            return self
        return None

    @staticmethod
    def get_subtags():
        return Subtag.query.all()





class PortfolioItemDB(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_desc = db.Column(db.String(255), nullable=False)
    long_desc = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary, nullable=True)
    demo_link = db.Column(db.String(255), nullable=True)
    github_link = db.Column(db.String(255), nullable=True)

    # Add fields to link with tags and subtags tables
    tags = relationship(
        'Tag',
        secondary=tags_to_items,
        primaryjoin=(id == tags_to_items.c.itemid),
        secondaryjoin=(Tag.id == tags_to_items.c.tagid),
        backref='items'
    )

    subtags = relationship(
        'Subtag',
        secondary=subtags_to_items,
        primaryjoin=(id == subtags_to_items.c.itemid),
        secondaryjoin=(Subtag.id == subtags_to_items.c.subtagid),
        backref='items'
    )



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

