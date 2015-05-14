from app import app
from flask import request, render_template, redirect, url_for, flash
from flask.ext.login import login_required, current_user, login_user, logout_user
from models import *
from forms_admin import *
from datetime import datetime
from utility import accepted_roles
from utility import slugify
from sqlalchemy import desc
from dateutil.parser import parse
from utility import bbparser


@app.route('/admin', methods=['GET'])
@login_required
@accepted_roles('admin')
def index_admin():
    return render_template('admin/index-admin.html')


@app.route('/admin/articles', methods=['GET'])
@app.route('/admin/articles/<int:page>', methods=['GET'])
@login_required
@accepted_roles('admin')
def articles(page=1):
    the_articles = Article.query.order_by(desc(Article.created_at)).paginate(page,
        app.config['ARTICLES_PER_PAGE_ADMIN'], True)
    return render_template('admin/articles.html', articles=the_articles)


@app.route('/admin/articles/add', methods=['GET'])
@login_required
@accepted_roles('admin')
def article_add():
    form = ArticleAddForm()
    form.tag.choices = ([(a.id, a.name) for a in Tag.query.all()])
    return render_template('admin/article-add.html', form=form)


@app.route('/admin/articles/add', methods=['POST'])
@login_required
@accepted_roles('admin')
def article_add_post():
    form = ArticleAddForm()
    form.tag.choices = ([(a.id, a.name) for a in Tag.query.all()])
    if form.validate_on_submit():
        # Slugify the URL
        the_slug = form.slug.data
        the_title = form.title.data
        if not the_slug:
            the_slug = slugify(the_title)
        # Parse the bbcode into html
        the_html = bbparser.format(form.body.data)

        article = Article(title=the_title,
                          slug=the_slug,
                          tag=form.tag.data,
                          body=form.body.data,
                          html=the_html,
                          created_at=datetime.utcnow(),
                          modified_at=datetime.utcnow(),
                          user_id=current_user.id,
                          visible=True)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('articles'))
    return render_template('admin/article-add.html', form=form)


@app.route('/admin/articles/detail/<article_id>', methods=['GET'])
@login_required
@accepted_roles('admin')
def article_detail(article_id):
    form = ArticleDetailForm()
    form.tag.choices = ([(a.id, a.name) for a in Tag.query.all()])
    article = Article.query.get_or_404(article_id)

    form.title.data = article.title
    form.slug.data = article.slug
    form.tag.data = article.tag
    form.visible.data = article.visible
    form.created_at.data = article.created_at
    form.body.data = article.body

    return render_template('admin/article-detail.html', form=form, article=article)


@app.route('/admin/articles/detail/<article_id>', methods=['POST'])
@login_required
@accepted_roles('admin')
def article_detail_post(article_id):
    form = ArticleDetailForm()
    form.tag.choices = ([(a.id, a.name) for a in Tag.query.all()])
    article = Article.query.get_or_404(article_id)

    if form.validate_on_submit():
        article.title = form.title.data
        article.slug = form.slug.data
        article.tag = form.tag.data
        article.visible = form.visible.data
        article.created_at = parse(form.created_at.data)
        article.body = form.body.data
        article.html = bbparser.format(form.body.data)

        db.session.add(article)
        db.session.commit()
        flash("Updated successfully")
        return redirect(url_for('articles'))
    return render_template('admin/article-detail.html', form=form, article=article)


@app.route('/admin/articles/delete/<article_id>', methods=['GET'])
@login_required
@accepted_roles('admin')
def article_delete(article_id):
    form = ConfirmForm()
    article = Article.query.get_or_404(article_id)
    return render_template('admin/article-delete.html', form=form, article=article)


@app.route('/admin/articles/delete/<article_id>', methods=['POST'])
@login_required
@accepted_roles('admin')
def article_delete_post(article_id):
    form = ConfirmForm()
    article = Article.query.get_or_404(article_id)
    if form.validate_on_submit():
        db.session.delete(article)
        db.session.commit()
        flash('Deleted %s' % article.title)
        return redirect(url_for('articles'))
    return render_template('admin/article-delete.html', form=form, article=article)


@app.route('/admin/users', methods=['GET'])
@app.route('/admin/users/<int:page>', methods=['GET'])
@login_required
@accepted_roles('admin')
def users(page=1):
    the_users = User.query.order_by(desc(User.created_at)).paginate(page, app.config['ARTICLES_PER_PAGE_ADMIN'], True)
    return render_template('admin/users.html', users=the_users)


@app.route('/admin/users/detail/<user_id>', methods=['GET'])
@login_required
@accepted_roles('admin')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/user-detail.html', user=user)


@app.route('/admin/categories', methods=['GET'])
@login_required
@accepted_roles('admin')
def tags():
    the_categories = Tag.query.order_by(Tag.name)
    return render_template('admin/tags.html', categories=the_categories)


@app.route('/admin/categories/add', methods=['GET'])
@login_required
@accepted_roles('admin')
def tag_add():
    form = TagAddForm()
    return render_template('admin/tag-add.html', form=form)


@app.route('/admin/categories/add', methods=['POST'])
@login_required
@accepted_roles('admin')
def tag_add_post():
    form = TagAddForm()
    if form.validate_on_submit():
        # Slugifying the URL
        the_slug = form.slug.data
        the_name = form.name.data
        # If the slug form field is left empty, auto generate the slug
        if not the_slug:
            the_slug = slugify(the_name)
        tag = Tag(name=the_name, slug=the_slug)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('tags'))
    return render_template('admin/tag-add.html', form=form)
