from app import app, db, login_manager
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role: %s>' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('User', lazy='dynamic'))
    articles = db.relationship('Article', backref='User', lazy='dynamic')

    def __init__(self, email, username, password):
        # Normalize the email by stripping whitespace and lowercasing
        self.email = email.strip().lower()
        self.username = username
        # Hash the password
        self.hash_password(password)
        # Give the new user a default role, make sure to create this role first
        default_role = Role.query.filter_by(name=app.config['DEFAULT_ROLE']).first()
        self.roles.append(default_role)
        self.active = True
        self.created_at = datetime.utcnow()

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User: %s>' % self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    created_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    visible = db.Column(db.Boolean())
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __repr__(self):
        return '<Comment: %s>' % self.body


class Tag(db.Model):
    __searchable__ = ['name', 'slug']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    slug = db.Column(db.Text)
    articles = db.relationship('Article', backref='Tag', lazy='dynamic')

    def __repr__(self):
        return '<Tag: %s>' % self.name


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    slug = db.Column(db.Text)
    created_at = db.Column(db.DateTime())
    modified_at = db.Column(db.DateTime())
    publish_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    visible = db.Column(db.Boolean())
    tag = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __repr__(self):
        return '<Article: %s>' % self.title
