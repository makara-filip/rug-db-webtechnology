from flask import redirect, url_for, render_template, flash
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa

from app import app, db
from app.models import User, get_user_by_username
from app.forms import LoginForm, RegistrationForm

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", current_user=current_user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    
    logout_user()
    return redirect(url_for("index"))
    
@app.route("/registration", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)
