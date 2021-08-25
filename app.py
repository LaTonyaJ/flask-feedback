from flask.helpers import flash
from flask.templating import render_template
from forms import Register, Login, FeedbackForm, EditFeedbackForm
from flask import Flask, request, redirect, session
from werkzeug.utils import redirect
from models import connect_db, db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
import pdb

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
    """Redirect to register"""

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def create_user():
    """Register a new user"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = Register()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data.lower()
        password = form.password.data
        email = form.email.data

        new_user = User.register(
            username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = new_user.username
        flash('User added!')
        return redirect(f'/users/{new_user.username}')

    else:
        return render_template('user_form.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    """Display User info"""

    if "username" in session:

        user = User.query.get(username)
        return render_template('user.html', user=user)

    else:
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def user_login_form():
    """User login"""

    if 'username' in session:
        return redirect(f"/users/{session['username']}")

    form = Login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        new_user = User.authenticate(username, password)

        if new_user:
            session['username'] = new_user.username.lower()
            return redirect(f'/users/{new_user.username}')
        else:
            form.username.errors = ['Invalid username/password']
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log out user"""

    session.pop('username')
    return redirect('/login')


@app.route('/users/<username>/delete')
def delete_user(username):
    """Delete User"""

    user = User.query.get(username)

    if 'username' in session and username == user.username:
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash('User Deleted!')

        return redirect('/')
    else:
        return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def show_feedback_form(username):
    """Add Feedback"""

    form = FeedbackForm()
    # pdb.set_trace()
    if 'username' in session and username == session['username']:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            fb = Feedback(title=title, content=content, username=username)

            db.session.add(fb)
            db.session.commit()

            return redirect(f'/users/{username}')
        else:
            return render_template('add_feedback.html', form=form)

    else:
        return render_template('add_feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Edit Feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' in session and feedback.username == session['username']:

        form = EditFeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.commit()

            return redirect(f'/users/{feedback.username}')

        return render_template('edit_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['GET', 'POST'])
def delete_feedback(feedback_id):
    """Delete Feedback"""

    feedback = Feedback.query.get(feedback_id)

    if 'username' in session and feedback.username == session['username']:

        db.session.delete(feedback)
        db.session.commit()

        return redirect(f'/users/{feedback.username}')

    return render_template(f'/users/{feedback.username}')
