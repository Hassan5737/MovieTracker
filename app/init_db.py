

from app import app, db
from app.models import Movie

with app.app_context():
    db.create_all()
    print("Tables created!")
