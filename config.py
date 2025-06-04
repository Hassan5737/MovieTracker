import os

class Config:
    # إعداد الاتصال بقاعدة بيانات PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:2004@localhost/movietracker"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "devkey"
