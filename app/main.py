from flask import Blueprint, render_template, jsonify, request, flash, url_for, redirect
from flask_login import current_user, login_required
from . import db
from .models import Movie, Tag, Review, Like
from sqlalchemy.exc import IntegrityError
main = Blueprint('main', __name__)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tag_id = request.args.get('tag_id')

    query = Movie.query
    if tag_id and tag_id.isdigit():
        tag = Tag.query.get(int(tag_id))
        if tag:
            query = tag.movies

    pagination = query.paginate(page=page, per_page=8)
    movies = pagination.items
    tags = Tag.query.all()
    return render_template('index.html', movies=movies, tags=tags, pagination=pagination)


@main.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.create_time.desc()).all()
    tags = Tag.query.all()

    if request.method == 'POST' and current_user.is_authenticated:
        content = request.form.get('review_content', '').strip()
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


@main.route('/movies/<int:movie_id>/like', methods=['POST'])
@login_required
def like_movie(movie_id):
    # 1. 验证电影存在
    movie = Movie.query.get_or_404(movie_id)

    try:
        # 2. 通过关联关系判断是否已点赞（无需查询user_like表）
        if movie in current_user.liked_movies:
            # 已点赞：取消点赞（从用户点赞列表中移除）
            current_user.liked_movies.remove(movie)
            db.session.commit()
            return jsonify({
                'success': True,
                'liked': False,
                'msg': '取消点赞成功（已更新user_like表）'
            })
        else:
            # 未点赞：添加点赞（将电影加入用户点赞列表）
            current_user.liked_movies.append(movie)
            db.session.commit()
            return jsonify({
                'success': True,
                'liked': True,
                'msg': '点赞成功（已写入user_like表）'
            })

    except Exception as e:
        db.session.rollback()
        print(f"点赞操作报错：{e}")
        return jsonify({
            'success': False,
            'message': f'操作失败：{str(e)}'
        }), 500

@main.route('/recommend')
@login_required
def recommend():
    liked_tag_ids = set()
    for movie in current_user.liked_movies:
        for tag in movie.tags:
            liked_tag_ids.add(tag.id)

    if not liked_tag_ids:
        flash('暂无点赞记录，无法生成个性化推荐', 'info')
        return redirect(url_for('main.index'))

    liked_movie_ids = [m.id for m in current_user.liked_movies]
    recommended_movies = Movie.query.filter(
        Movie.tags.any(Tag.id.in_(liked_tag_ids)),
        ~Movie.id.in_(liked_movie_ids)
    ).distinct().limit(5).all()

    tags = Tag.query.all()
    return render_template('recommend.html', movies=recommended_movies, tags=tags)


@main.route('/search')
def search_movies():
    query = request.args.get('query', '')
    if query:
        movies = Movie.query.filter(Movie.title.like(f'%{query}%')).all()
    else:
        movies = []
    return render_template('search_results.html', movies=movies, query=query)

# 个人中心路由（需要登录才能访问）
@main.route('/profile')
@login_required
def profile():
    """个人界面：展示用户信息及点赞的电影"""
    # 直接通过关联属性获取当前用户点赞的所有电影，无需手动查询关联表
    liked_movies = current_user.liked_movies
    return render_template('profile.html', user=current_user, liked_movies=liked_movies)