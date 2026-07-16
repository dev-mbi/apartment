import os
import tempfile
import pytest
from sqlalchemy.pool import StaticPool


@pytest.fixture
def app():
    from config import Config

    old_uri = Config.SQLALCHEMY_DATABASE_URI
    Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    old_engine_opts = getattr(Config, 'SQLALCHEMY_ENGINE_OPTIONS', None)
    Config.SQLALCHEMY_ENGINE_OPTIONS = {'poolclass': StaticPool}

    from app import create_app, db as _db
    application = create_app()

    yield application

    Config.SQLALCHEMY_DATABASE_URI = old_uri
    if old_engine_opts is not None:
        Config.SQLALCHEMY_ENGINE_OPTIONS = old_engine_opts
    else:
        del Config.SQLALCHEMY_ENGINE_OPTIONS


@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c


@pytest.fixture
def db(app):
    from app import db
    with app.app_context():
        yield db


@pytest.fixture
def auth(client, app):
    from app import db
    from models.user import User
    from werkzeug.security import generate_password_hash

    with app.app_context():
        user = User(
            username='admin',
            email='admin@test.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(user)
        db.session.commit()

    client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    return client
