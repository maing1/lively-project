from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

bcrypt = Bcrypt() 
from config import db


# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    bio = db.Column(db.Text, default="")
    profile_picture = db.Column(db.String, default="")
    posts = db.relationship('Post', back_populates='user', lazy=True)
    followers = db.relationship(
        'Follower',
        foreign_keys='Follower.followed_id',
        backref='followed_user',
        lazy=True
    )
    following = db.relationship(
        'Follower',
        foreign_keys='Follower.follower_id',
        backref='follower_user',
        lazy=True
    )

    @validates('username')
    def validate_username(self,key,value):
        if len(value) < 3:
            ValueError('name must be 3 characters and above')
        return value
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password.encode('utf-8')).decode("utf-8")

    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash,password.encode('utf-8'))


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    caption = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, default="")
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

     # Relationship: One-to-Many (Post -> User)
    user = db.relationship('User', back_populates='posts')

    @property
    def username(self):
        """Access the username of the user who created the post."""
        return self.user.username


class Like(db.Model, SerializerMixin):
    __tablename__ = 'Likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)


class Follower(db.Model, SerializerMixin):
    __tablename__ = 'followers'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)