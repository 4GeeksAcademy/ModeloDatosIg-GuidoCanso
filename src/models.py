from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), nullable=False, unique=True)
    email = db.Column(String(100), nullable=False, unique=True)
    profile_picture = db.Column(String(250))

    # Relaciones entre las tablas
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    followers = relationship(
        "Follower", foreign_keys='Follower.user_id', back_populates="user")
    following = relationship(
        "Follower", foreign_keys='Follower.follower_id', back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "profile_picture": self.profile_picture
        }


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(Integer, primary_key=True)  # Clave primaria
    # URL de la imagen (obligatoria)
    image_url = db.Column(String(250), nullable=False)
    caption = db.Column(String(250))  # Descripción o texto del post (opcional)
    # Relación con el autor (usuario)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))

    # Relación inversa: este post pertenece a un usuario
    user = relationship("User", back_populates="posts")

    # Relación con comentarios y likes
    comments = relationship("Comment", back_populates="post")
    likes = relationship("Like", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "user_id": self.user_id
        }


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(Integer, primary_key=True)  # Clave primaria
    # Texto del comentario (obligatorio)
    text = db.Column(String(250), nullable=False)
    # Relación con el usuario que comenta
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    # Relación con el post sobre el que se comenta
    post_id = db.Column(Integer, db.ForeignKey('post.id'))

    # Relación inversa: el comentario pertenece a un usuario
    user = relationship("User", back_populates="comments")
    # Relación inversa: el comentario pertenece a un post
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Like(db.Model):
    __tablename__ = 'like'

    id = db.Column(Integer, primary_key=True)  # Clave primaria
    user_id = db.Column(Integer, db.ForeignKey('user.id'))  # Quién dio like
    post_id = db.Column(Integer, db.ForeignKey(
        'post.id'))  # A qué post le dio like

    # Relaciones inversas
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Follower(db.Model):
    __tablename__ = 'follower'

    id = db.Column(Integer, primary_key=True)  # Clave primaria

    # El usuario que está siendo seguido
    user_id = db.Column(Integer, db.ForeignKey('user.id'))

    # El usuario que sigue
    follower_id = db.Column(Integer, db.ForeignKey('user.id'))

    # Relaciones inversas con alias para que no se confunda
    user = relationship("User", foreign_keys=[
                        user_id], back_populates="followers")
    follower = relationship("User", foreign_keys=[
                            follower_id], back_populates="following")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,  # A quién sigo
            "follower_id": self.follower_id  # Quién me sigue
        }


render_er(db.Model, 'diagram.png')
