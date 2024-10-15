from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates 
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Association table
user_groups=db.Table('user_groups',
                     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                     db.Column('group_id', db.Integer, db.ForeignKey('groups.id')))

class User(db.Model, SerializerMixin):
    __tablename__ ='users'

    serialize_rules=('-posts.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(225))

    # relationships with post
    posts = db.relationship('Post', back_populates='user')
    groups = db.relationship('Group', secondary=user_groups, back_populates='users')

    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError('Invalid email address')
        return value

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    serialize_rules=('-user.posts', '-user.groups',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships with user
    user = db.relationship('User', back_populates='posts')

class Group(db.Model, SerializerMixin):
    __tablename__ = 'groups'

    serialize_rules=('-users.groups',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # relationships
    users = db.relationship('User', secondary=user_groups, back_populates='groups')

