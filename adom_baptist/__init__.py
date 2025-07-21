from flask import Flask, session
from dotenv import load_dotenv
import os
from extensions import db, migrate, mail 

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    # Load config
    app.config.from_object('config.Config')
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Initialize extensions
    try:
        db.init_app(app)
        print("Database connected successfully.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    
    migrate.init_app(app, db)
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'
    mail.init_app(app)

    #Blueprints register
    from .routes.main_routes import main_bp
    
    app.register_blueprint(main_bp)
    return app
