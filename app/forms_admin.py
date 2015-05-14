from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms import ValidationError
from models import *
from sqlalchemy import func


class ArticleAddForm(Form):
    title = StringField('Title')
    slug = StringField('Slug')
    tag = SelectField('Tag', coerce=int)
    body = TextAreaField('Body')
    submit = SubmitField('Add Article')


class ArticleDetailForm(Form):
    title = StringField('Title')
    slug = StringField('Slug')
    tag = SelectField('Tag', coerce=int)
    visible = BooleanField('Visible')
    created_at = StringField('Created Date')
    body = TextAreaField('Body')
    submit = SubmitField('Update')


class ConfirmForm(Form):
    confirm = BooleanField('Confirm')
    submit = SubmitField('Submit')


class TagAddForm(Form):
    name = StringField('Name')
    slug = StringField('Slug')
    submit = SubmitField('Add Category')

    def validate_name(self, field):
        # Normalize the names before checking for duplicates
        if Tag.query.filter(func.lower(Tag.name) == func.lower(field.data)).first():
            raise ValidationError('Tag already exist')
