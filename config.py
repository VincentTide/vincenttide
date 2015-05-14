import os

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'insert-secret-key'
SITE_TITLE = 'vincenttide'
DEFAULT_ROLE = 'user'
ARTICLES_PER_PAGE_HOMEPAGE = 10
ARTICLES_PER_PAGE_ADMIN = 20

from config_dev import *