import os

# 获取项目根目录（movie_review_app 文件夹）的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 修正：当前文件在 movie_review_app 目录下，直接取当前目录的父路径即可
# 定义数据库文件路径到 instance 文件夹
DB_PATH = os.path.join(BASE_DIR, 'instance', 'movie_review.db')  # 新增 instance 目录层级

class Config:
    # 数据库配置（使用新的 DB_PATH）
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key_123456'
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
