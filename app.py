from flask.helpers import flash
from flask.templating import render_template
from forms import Register, Login
from flask import Flask, request, redirect
from werkzeug.utils import redirect
from models import connect_db, db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.config['SECRET_KEY'] = 'user-feedback-demo'
debug = DebugToolbarExtension(app)


@app.route('/')
def show_homepage():

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def create_user():

    form = Register()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        email = form.email.data

        new_user = User(first_name=first_name, last_name=last_name,
                        username=username, password=password, email=email)

        db.session.add(new_user)
        db.session.commit()
        flash('User added!')
        return redirect('/secret')

    else:
        return render_template('user_form.html', form=form)


@app.route('/secret')
def show_secret():

    return render_template('secret.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login_form():

    form = Login()

    return render_template('login.html', form=form)
