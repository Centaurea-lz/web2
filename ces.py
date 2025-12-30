# 替换为你的项目路径和模型导入
import sys
sys.path.append("D:\python\movie_review_app")  # 项目根目录

from app import app, db
from app.models import User, Movie, Like

# 绑定应用上下文
with app.app_context():
    # 确保存在用户（id=1）和电影（id=2，对应你报错的movie_id=2）
    user = User.query.get(1)
    movie = Movie.query.get(2)
    if user and movie:
        # 手动创建点赞记录
        new_like = Like(user_id=user.id, movie_id=movie.id)
        db.session.add(new_like)
        try:
            db.session.commit()
            print("手动插入点赞记录成功！")
            # 查询验证
            like = Like.query.filter_by(user_id=1, movie_id=2).first()
            if like:
                print(f"验证成功：查询到点赞记录 {like.id}")
            else:
                print("手动插入后查询不到，表结构或会话有问题")
        except Exception as e:
            db.session.rollback()
            print(f"手动插入失败：{e}")
    else:
        print("用户id=1或电影id=2不存在，请先确认数据")
