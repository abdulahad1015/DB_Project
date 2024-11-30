from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Bootstrap5(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
                          
    @app.before_request
    def make_session_non_permanent():
        session.permanent = False

    # Import routes within app context to avoid circular imports
    with app.app_context():
        from . import routes

    return app