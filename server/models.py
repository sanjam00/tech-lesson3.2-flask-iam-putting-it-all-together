from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String)
  _password_hash = db.Column(db.String)

  # connects to posts table
  posts = db.relationship('Post', back_populates = 'user')

  # Authorization methods
  # protects password hashes from being viewed
  @hybrid_property
  def password_hash(self):
    return AttributeError("Password hashes may not be viewed.")

  # what does this do.... sets the password? hashes it?
  @password_hash.setter
  def password_hash(self, password):
    password_hash = bcrypt.generate_password_hash(
      password.encode('utf-8')
    )
    self._password_hash = password_hash.decode('utf-8')

  # authenticates the user; compares the stored hashed password against the inputed hashed password
  def authenticate(self, password):
    return bcrypt.check_password_hash(
      self._password_hash, password.encode('utf-8')
    )

  def __repr__(self):
    return f'<User {self.username}>, ID {self.id}'
  
class Post(db.Model):
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key = True)
  content = db.Column(db.String)

  # establish relationship between tables
  # one to many relationship, so this side has the foreign key for users since it's the "many" side
  user_id = db.Column(db.Inteteger(), db.ForeignKey('users.id'))
  user = db.relationship('User', back_populates = 'posts')

  def __repr__(self):
    return f'<Post {self.id}>: {self.content}'
  