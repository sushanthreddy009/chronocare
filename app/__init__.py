import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your-secret-key'  # needed for sessions

    # Configure Flask-Mail
    app.config.update(
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME='sushanthreddy717@gmail.com',
        MAIL_PASSWORD='xbrfvufapiwsrtbz',
        MAIL_DEFAULT_SENDER='sushanthreddy717@gmail.com'
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    from .routes import auth
    app.register_blueprint(auth)

    return app