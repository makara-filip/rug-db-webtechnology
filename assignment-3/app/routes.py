from flask import redirect, url_for, render_template, flash, request, abort
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from werkzeug.exceptions import NotFound

from app import app, db
from app.models import User, Movie, get_user_by_username
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

@app.route("/movies")
@login_required
def movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    movie = None
    
    if request.method == "GET":
        if "id" in request.args:
            # Fetch the movie by ID if it exists
            movie_id = request.args["id"]
            movie = Movie.query.get(movie_id)
            if not movie:
                abort(NotFound.code, description="Movie not found")
        return render_template("add_movie.html", movie=movie)

    # else, the method is POST
    movie_id = request.form["id"]
    if movie_id:
        # Edit the existing movie
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(NotFound.code, description="Movie not found")
        
        movie.name = request.form["name"]
        movie.year = request.form["year"]
        movie.awards = request.form["awards"]
    else:
        # Create a new Movie entry
        movie = Movie(
            name=request.form["name"],
            year=request.form["year"],
            awards=request.form["awards"]
        )

    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('add_movie', id=movie.id))

@app.route('/delete_movie', methods=['POST'])
@login_required
def delete_movie():
    if "id" not in request.args:
        return "Movie id not specified", 400
    
    # Get the movie by ID
    movie_id = request.args["id"]
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(NotFound.code, description="Movie not found")
    
    try:
        # Delete the movie from the database
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('movies'))
    except:
        return "There was a problem deleting that movie.", 500

@app.errorhandler(NotFound.code)
def page_not_found(exception):
    return render_template('error.html', exception=exception), 404
