from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_pwd = request.form.get('confirm_pwd')

        # 表单验证
        if not username or not email or not password:
            flash('所有字段不能为空！', 'danger')
            return redirect(url_for('auth.register'))
        if password != confirm_pwd:
            flash('两次密码不一致！', 'danger')
            return redirect(url_for('auth.register'))
        if len(password) < 6:
            flash('密码长度不能少于6位！', 'danger')
            return redirect(url_for('auth.register'))

        # 检查用户名/邮箱是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已被注册！', 'danger')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册！', 'danger')
            return redirect(url_for('auth.register'))

        # 创建新用户
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功！请登录', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        # 查询用户
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('用户名或密码错误！', 'danger')
            return redirect(url_for('auth.login'))

        # 登录用户
        login_user(user)
        flash('登录成功！', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已成功退出登录！', 'info')
    return redirect(url_for('main.index'))
