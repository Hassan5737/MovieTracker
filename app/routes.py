import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Movie

main = Blueprint("main", __name__)

TMDB_API_KEY = '09fc0258e73b7bd2b3b4cc1b23fc7bc4'
TMDB_API_URL = 'https://api.themoviedb.org/3/search/movie'

def get_movie_details(title):
    response = requests.get(TMDB_API_URL, params={
        'api_key': TMDB_API_KEY,
        'query': title
    })

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            movie_data = data['results'][0]
            return {
                'title': movie_data['title'],
                'description': movie_data['overview'],
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data['poster_path'] else None,
                'year': movie_data['release_date'][:4],
                'rating': movie_data.get('vote_average', 'N/A')
            }
    return None

@main.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form.get("title")

        if not title:
            flash("Please enter a movie title.")
            return redirect(url_for("main.add_movie"))

        movie_details = get_movie_details(title)

        if not movie_details:
            flash("Movie not found.")
            return redirect(url_for("main.add_movie"))

        movie = Movie(
            title=movie_details['title'],
            year=movie_details['year'],
            genre="",
            director="",
            poster_url=movie_details['poster_url'],
            description=movie_details['description']
        )

        db.session.add(movie)
        db.session.commit()
        flash("Movie added successfully!")
        return redirect(url_for("main.add_movie"))

    return render_template("add_movie.html")

@main.route("/movies")
def movie_list():
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)

@main.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template("movie_detail.html", movie=movie)

@main.route("/movie/edit/<int:movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        movie.title = request.form.get("title")
        movie.description = request.form.get("description")
        movie.poster_url = request.form.get("poster_url")
        movie.rating = request.form.get("rating")

        db.session.commit()
        flash("Movie details updated successfully!")
        return redirect(url_for("main.movie_detail", movie_id=movie.id))

    return render_template("edit_movie.html", movie=movie)

@main.route("/movie/delete/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Movie deleted successfully!")
    return redirect(url_for("main.movie_list"))

# ✅ ده الراوت الجديد اللي يوجّه للصفحة الرئيسية
@main.route("/")
def index():
    return redirect(url_for("main.movie_list"))
