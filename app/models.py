from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    poster_url = db.Column(db.String(200))
    year = db.Column(db.String(4))
    rating = db.Column(db.Float)
    genre = db.Column(db.String(120))
    director = db.Column(db.String(120))  # اضفت ده

    def __repr__(self):
        return f"<Movie {self.title}>"
