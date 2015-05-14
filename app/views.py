from app import app
from flask import request, render_template, redirect, url_for, flash, abort
from flask.ext.login import login_required, current_user, login_user, logout_user
from models import *
from forms import *
from sqlalchemy import desc
import random
from utility import bbparser


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/', methods=['GET'])
@app.route('/index/<int:page>', methods=['GET'])
def index(page=1):
    articles = Article.query.filter_by(visible=True).order_by(desc(Article.created_at)).paginate(page,
        app.config['ARTICLES_PER_PAGE_HOMEPAGE'], True)
    return render_template('index.html',
                           articles=articles)


# @app.route('/register', methods=['GET'])
# def register():
#     form = RegistrationForm()
#     return render_template('auth/register.html', form=form)


# @app.route('/register', methods=['POST'])
# def register_post():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(email=form.email.data,
#                     username=form.username.data,
#                     password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@app.route('/login', methods=['POST'])
def login_post():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/permission-denied', methods=['GET'])
def permission_denied():
    return render_template('permission-denied.html')


@app.route('/news/<article_id>/<slug>', methods=['GET'])
def article_single(article_id, slug):
    the_article = Article.query.get_or_404(article_id)
    if the_article.slug == slug:
        return render_template('article-single.html',
                               article=the_article)
    else:
        abort(404)


@app.route('/tools', methods=['GET'])
def tools():
    return render_template('tools.html')


@app.route('/contact-us', methods=['GET'])
def contact_us():
    return render_template('contact-us.html')

