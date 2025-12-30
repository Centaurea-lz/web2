from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 多对多关联表：电影-标签
movie_tag = db.Table(
    'movie_tag',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# 多对多关联表：用户-点赞电影
user_like = db.Table(
    'user_like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # 关联评论
    reviews = db.relationship('Review', backref='author', lazy=True, cascade="all, delete-orphan")
    # 关联点赞的电影 —— 关键修改：移除 lazy='dynamic'
    liked_movies = db.relationship('Movie', secondary=user_like, backref='likers')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    poster_url = db.Column(db.String(200), default="https://via.placeholder.com/300x450?text=No+Poster")
    # 多对多关联标签
    tags = db.relationship('Tag', secondary=movie_tag, backref=db.backref('movies', lazy='dynamic'))
    # 关联评论
    reviews = db.relationship('Review', backref='movie', lazy=True, cascade="all, delete-orphan")


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=5)  # 1-5分
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 关联用户
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)  # 关联电影
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 确保一个用户只能给一个电影点一次赞（唯一约束）
    __table_args__ = (db.UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_like'),)