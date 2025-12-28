import sys
import os

# 把项目根目录加入Python搜索路径（解决导入问题）
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models import Movie

# 配置你要修改的参数（改这里就行！）
TARGET_MOVIE_TITLE = "星际穿越"  # 要修改的电影标题（精确匹配）
NEW_RELEASE_YEAR = 2015  # 新的上映年份
NEW_POSTER_NAME = "Interstellar.jpg"  # 新的海报文件名（需放到static/posters/）


def update_movie_info():
    # 创建Flask应用并进入上下文（必须）
    app = create_app()
    with app.app_context():
        # 1. 查找目标电影
        movie = Movie.query.filter_by(title=TARGET_MOVIE_TITLE).first()

        if not movie:
            print(f"❌ 未找到电影：{TARGET_MOVIE_TITLE}")
            # 列出所有电影，方便核对标题
            all_movies = Movie.query.all()
            print("\n当前数据库中的电影列表：")
            for m in all_movies:
                print(f"- 标题：{m.title} | 年份：{m.release_year} | 海报：{m.poster}")
            return

        # 2. 打印修改前的信息（调试用）
        print("=" * 50)
        print(f"修改前 - 《{movie.title}》")
        print(f"  上映年份：{movie.release_year}")
        print(f"  海报文件名：{movie.poster}")
        print("=" * 50)

        # 3. 执行修改
        movie.release_year = NEW_RELEASE_YEAR  # 修改上映年份
        movie.poster = NEW_POSTER_NAME  # 修改海报文件名

        # 4. 提交到数据库（核心！缺一不可）
        db.session.commit()

        # 5. 重新查询，验证修改是否生效
        updated_movie = Movie.query.filter_by(title=TARGET_MOVIE_TITLE).first()
        print(f"修改后 - 《{updated_movie.title}》")
        print(f"  上映年份：{updated_movie.release_year}")
        print(f"  海报文件名：{updated_movie.poster}")
        print("=" * 50)
        print("✅ 电影信息修改成功！")

        # 6. 温馨提示
        print(f"\n📌 请确保新海报文件已放到：app/static/posters/{NEW_POSTER_NAME}")
        print("📌 修改后需重启Flask项目，页面才会显示新数据！")


if __name__ == "__main__":
    update_movie_info()
