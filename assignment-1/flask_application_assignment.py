import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the server
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Movie model representing the movies table
class Movie(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    awards = db.Column(db.Integer)

# Create the database and the tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    # Get all movies from the database
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    movie = None
    
    if request.method == "GET":
        if "id" in request.args:
            # Fetch the movie by ID if it exists
            movie_id = request.args["id"]
            movie = Movie.query.get(movie_id)
            if not movie:
                return "Movie not found.", 404
        return render_template("add_movie.html", movie=movie)

    # else, the method is POST
    movie_id = request.form["id"]
    if movie_id:
        # Edit the existing movie
        # movie_id = request.form["id"]
        movie = Movie.query.get(movie_id)
        if movie is None:
            return "Movie not found.", 404
        
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
def delete_movie():
    if "id" not in request.args:
        return "Movie id not specified", 400
    
    # Get the movie by ID
    movie_id = request.args["id"]
    movie = Movie.query.get(movie_id)
    if not movie:
        return "Movie not found", 404
    
    try:
        # Delete the movie from the database
        db.session.delete(movie)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was a problem deleting that movie.", 500

if __name__ == '__main__':
    app.run(debug=True)