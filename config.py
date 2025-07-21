import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Default secret key for development if not set in .env
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # SQLite DB absolute path
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory for product image uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'adom_baptist', 'static', 'uploads')

    

