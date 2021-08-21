from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms import validators
from wtforms.fields.simple import PasswordField, TextAreaField
from wtforms.validators import Email, InputRequired


class Register(FlaskForm):

    first_name = StringField('First Name', validators=[
                             validators.Length(min=1, max=30), InputRequired()])

    last_name = StringField('Last Name', validators=[
                            validators.Length(min=1, max=30), InputRequired()])

    username = StringField('Username', validators=[
                           validators.Length(min=1, max=20), InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])

    email = StringField('Email', validators=[
                        validators.Email(), validators.Length(max=50)])


class Login(FlaskForm):

    username = StringField('Username', validators=[
                           validators.Length(max=20), InputRequired()])

    password = PasswordField('Password', validators=[
                             validators.Length(max=50), InputRequired()])


class Feedback(FlaskForm):

    title = StringField('Title', validators=[
                        validators.Length(max=100), InputRequired()])

    content = TextAreaField('Content', validators=[InputRequired()])
