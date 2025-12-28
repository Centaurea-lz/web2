from flask import Blueprint, render_template, jsonify, request, flash, url_for, redirect
from flask_login import current_user, login_required
from . import db
from .models import Movie, Tag, Review, user_like
from sqlalchemy import desc  # 新增：可选，用于排序

main = Blueprint('main', __name__)


# 首页：影视列表
@main.route('/')
def index():
    # 获取页码参数，默认为第1页
    page = request.args.get('page', 1, type=int)
    # 支持按标签筛选
    tag_id = request.args.get('tag_id')

    # 构建查询对象
    query = Movie.query
    if tag_id and tag_id.isdigit():
        tag = Tag.query.get(int(tag_id))
        if tag:
            query = tag.movies  # 关联查询该标签下的电影

    # 分页查询（每页8条数据）
    pagination = query.paginate(page=page, per_page=8)
    movies = pagination.items  # 当前页的电影列表

    tags = Tag.query.all()
    # 将 pagination 传递给模板（用于前端分页控件）
    return render_template('index.html', movies=movies, tags=tags, pagination=pagination)
# 影视详情页（含评论功能）
@main.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    # 修正：通过Query对象查询评论并排序
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.create_time.desc()).all()
    tags = Tag.query.all()

    if request.method == 'POST' and current_user.is_authenticated:
        # 提交评论
        content = request.form.get('review_content').strip()
        rating = request.form.get('rating')
        if not content or not rating:
            flash('评论内容和评分不能为空！', 'danger')
        else:
            new_review = Review(
                content=content,
                rating=int(rating),
                user_id=current_user.id,
                movie_id=movie_id
            )
            db.session.add(new_review)
            db.session.commit()
            flash('评论提交成功！', 'success')
            return redirect(url_for('main.movie_detail', movie_id=movie_id))

    return render_template('movie_detail.html', movie=movie, reviews=reviews, tags=tags)


# AJAX点赞功能（高级功能）【修正路由语法】
@main.route('/like/<int:movie_id>', methods=['POST'])
@login_required
def like_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    # 判断是否已点赞
    if current_user in movie.likers:
        return jsonify({'success': False, 'msg': '已点赞过该影片'})
    # 添加点赞
    current_user.liked_movies.append(movie)
    db.session.commit()
    return jsonify({'success': True, 'msg': '点赞成功'})


# 影视推荐（高级功能：基于点赞标签推荐）
@main.route('/recommend')
@login_required
def recommend():
    # 获取用户点赞电影的所有标签ID
    liked_tag_ids = set()
    for movie in current_user.liked_movies:
        for tag in movie.tags:
            liked_tag_ids.add(tag.id)

    if not liked_tag_ids:
        flash('暂无点赞记录，无法生成个性化推荐', 'info')
        return redirect(url_for('main.index'))

    # 推荐逻辑：含相同标签且未点赞的电影
    recommended_movies = Movie.query.filter(
        Movie.tags.any(Tag.id.in_(liked_tag_ids)),
        Movie.id.notin_([m.id for m in current_user.liked_movies])
    ).distinct().limit(5).all()

    tags = Tag.query.all()
    return render_template('recommend.html', movies=recommended_movies, tags=tags)
