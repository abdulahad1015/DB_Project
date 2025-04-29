from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from prometheus_flask_exporter import PrometheusMetrics
import logging, sys
from pythonjsonlogger import jsonlogger

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ─── Core Flask extensions ─────────────────────────────────
    db.init_app(app)
    Bootstrap5(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # ─── Prometheus metrics  (/metrics) ────────────────────────
    metrics = PrometheusMetrics(app)            # auto-exposes /metrics
    metrics.info("app_info", "Application info", version="1.0.0")

    # ─── JSON logging to stdout (Loki-friendly) ───────────────
    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(
        jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(module)s %(message)s"
        )
    )
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)

    # ─── User loader for Flask-Login ───────────────────────────
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
           
    # ─── Make sessions non-permanent (original behaviour) ─────               
    @app.before_request
    def make_session_non_permanent():
        session.permanent = False

    # Import routes within app context to avoid circular imports
    with app.app_context():
        from . import routes

    return app