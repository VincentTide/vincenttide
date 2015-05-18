from functools import wraps
from flask import redirect, url_for
from flask.ext.login import current_user
from models import *
import re
from unicodedata import normalize
import bbcode


def get_current_user_role():
    user = User.query.filter_by(email=current_user.email).first()
    roles = []
    for role in user.roles:
        roles.append(role.name)
    return roles


def accepted_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_roles = get_current_user_role()
            permission = False
            for role in user_roles:
                if role in roles:
                    permission = True
            if not permission:
                return redirect(url_for('permission_denied'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


# Slugify
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


# BBCode Parser
def dev(tag_name, value, options, parent, context):
    return '<div class="dev">%s</div>' % value

def html(tag_name, value, options, parent, context):
    return value

def article_img(tag_name, value, options, parent, context):
    return '<div class="article_image"><img src="%s" /></div>' % value

def pre(tag_name, value, options, parent, context):
    return '<pre class="prettyprint">%s</pre>' % value

def code(tag_name, value, options, parent, context):
    return '<code class="prettyprint">%s</code>' % value


bbparser = bbcode.Parser()
bbparser.add_formatter('dev',
                       dev,
                       strip=True,
                       swallow_trailing_newline=True)
bbparser.add_formatter('html',
                       html,
                       escape_html=False,
                       swallow_trailing_newline=True,
                       transform_newlines=False,
                       replace_links=False,
                       replace_cosmetic=False)
bbparser.add_formatter('article_img',
                       article_img,
                       replace_links=False,
                       swallow_trailing_newline=True)
bbparser.add_formatter('pre',
                       pre)
bbparser.add_formatter('code',
                       code)
bbparser.add_simple_formatter('h1', '<h1>%(value)s</h1>')
bbparser.add_simple_formatter('h2', '<h2>%(value)s</h2>')
bbparser.add_simple_formatter('h3', '<h3>%(value)s</h3>')
bbparser.add_simple_formatter('h4', '<h4>%(value)s</h4>')
