from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Movie
import requests

main = Blueprint('main', __name__)

API_KEY = "09fc0258e73b7bd2b3b4cc1b23fc7bc4"  # استبدل بهذا الـ API key الخاص بك من TMDb

# صفحة الرئيسية لعرض الأفلام
@main.route('/')
def home():
    movies = Movie.query.all()  # استعلام لاسترجاع كل الأفلام من قاعدة البيانات
    return render_template('home.html', movies=movies)

# صفحة إضافة فيلم جديد
@main.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie_name = request.form['name']  # أخذ اسم الفيلم من المستخدم

        # طلب API للبحث عن الفيلم باستخدام اسم الفيلم
        url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}'
        response = requests.get(url)
        data = response.json()

        if data['results']:
            result = data['results'][0]  # أخذ أول نتيجة من البحث
            title = result['title']
            year = result['release_date'].split("-")[0] if result.get('release_date') else "N/A"
            description = result.get('overview', '')
            poster_url = f"https://image.tmdb.org/t/p/w500{result['poster_path']}" if result.get('poster_path') else ''

            # إضافة الفيلم إلى قاعدة البيانات
            movie = Movie(name=title, year=year, description=description, poster_url=poster_url)
            db.session.add(movie)
            db.session.commit()

        return redirect(url_for('main.home'))  # إعادة التوجيه إلى الصفحة الرئيسية بعد إضافة الفيلم

    return render_template('add_movie.html')  # عرض الصفحة لإضافة فيلم جديد
