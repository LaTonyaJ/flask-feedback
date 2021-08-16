from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms import validators
from wtforms.fields.simple import PasswordField
from wtforms.validators import Email


class Register(FlaskForm):

    first_name = StringField('First Name', validators=[
                             validators.Length(min=1, max=30)])

    last_name = StringField('Last Name', validators=[
                            validators.Length(min=1, max=30)])

    username = StringField('Username', validators=[
                           validators.Length(min=1, max=20)])

    password = PasswordField('Password')

    email = StringField('Email', validators=[
                        validators.Email(), validators.Length(max=50)])


class Login(FlaskForm):

    username = StringField('Username', validators=[validators.Length(max=20)])

    password = PasswordField('Password', validators=[
                             validators.Email(), validators.Length(max=50)])
