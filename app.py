from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name=None):
    app = Flask(__name__)
    cfg = config.get(config_name, config['default'])
    app.config.from_object(cfg)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from routes.auth_routes import auth_bp
    from routes.apartment_routes import apartment_bp
    from routes.masjid_routes import masjid_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(apartment_bp)
    app.register_blueprint(masjid_bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    with app.app_context():
        db.create_all()

    return app
