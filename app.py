from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from routes.auth_routes import auth_bp
    from routes.apartment_routes import apartment_bp
    from routes.masjid_routes import masjid_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(apartment_bp)
    app.register_blueprint(masjid_bp)

    with app.app_context():
        from models.user import User
        from models.apartment import Apartment, Resident, Complaint, MaintenanceRequest, Announcement
        from models.masjid import Donation, Expense
        db.create_all()

    return app
