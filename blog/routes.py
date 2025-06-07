# routes.py
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from models import User, Post, Like
from forms import RegistrationForm, LoginForm, PostForm
from extensions import db
from sqlalchemy import or_
def register_routes(app):
    # ---------- 所有路由必须在此函数内定义 ----------
    @app.route('/user/<username>')
    def user_profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
        return render_template('user_profile.html', user=user, posts=posts)

    @app.route('/post/<int:post_id>/like', methods=['POST'])
    @login_required
    def like_post(post_id):
        post = Post.query.get_or_404(post_id)
        # 检查是否已点赞
        existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if existing_like:
            db.session.delete(existing_like)
            db.session.commit()
            flash('已取消点赞', 'info')
        else:
            like = Like(user_id=current_user.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()
            flash('点赞成功！', 'success')
        return redirect(url_for('index'))
    
    @app.route('/')
    def index():
        posts = Post.query.all()
        return render_template('index.html', posts=posts)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            # 示例代码：实际需使用密码哈希
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('注册成功！请登录', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='注册', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('登录失败，请检查邮箱和密码', 'danger')
        return render_template('login.html', title='登录', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/post/new', methods=['GET', 'POST'])
    @login_required
    def new_post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('文章发布成功！', 'success')
            return redirect(url_for('index'))
        return render_template('create_post.html', title='写文章', form=form)

    @app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            abort(403)
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash('文章已更新！', 'success')
            return redirect(url_for('index'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('create_post.html', title='编辑文章', form=form)

    # routes.py
    @app.route('/search')
    def search():
        keyword = request.args.get('q', '')
        result_type = request.args.get('type', 'posts')  # 默认为文章搜索

        # 搜索文章
        if result_type == 'posts':
            posts = Post.query.filter(
                or_(
                    Post.title.ilike(f'%{keyword}%'),
                    Post.content.ilike(f'%{keyword}%')
                )
            ).all()
            users = []
    # 搜索用户
        elif result_type == 'users':
            users = User.query.filter(
                or_(
                    User.username.ilike(f'%{keyword}%'),
                    User.email.ilike(f'%{keyword}%')
                )
            ).all()
            posts = []
        else:
            posts = []
            users = []

        return render_template('search.html', 
            posts=posts, 
            users=users, 
            keyword=keyword,
            result_type=result_type  # 传递当前结果类型
        )    
    # routes.py
    @app.route('/follow/<username>')
    @login_required
    def follow(username):
        user = User.query.filter_by(username=username).first_or_404()
        if current_user == user:
            flash('不能关注自己', 'warning')
        else:
            current_user.follow(user)
            flash(f'已关注 {username}', 'success')
        return redirect(url_for('user_profile', username=username))

    @app.route('/unfollow/<username>')
    @login_required
    def unfollow(username):
        user = User.query.filter_by(username=username).first_or_404()
        current_user.unfollow(user)
        flash(f'已取消关注 {username}', 'info')
        return redirect(url_for('user_profile', username=username))
    # routes.py
    @app.route('/user/<username>/following')
    def following_list(username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('following.html', user=user)

    @app.route('/user/<username>/followers')
    def followers_list(username):
        user = User.query.filter_by(username=username).first_or_404()
        return render_template('followers.html', user=user)
    # routes.py
    # routes.py
   
    
    # ---------- 路由定义结束 ----------