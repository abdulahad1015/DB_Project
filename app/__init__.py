from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_bootstrap import Bootstrap5


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Bootstrap5(app)
    # Import routes within app context to avoid circular imports
    with app.app_context():
        from . import routes

    return app