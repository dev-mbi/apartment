import pytest


@pytest.fixture
def app():
    from app import create_app
    application = create_app('testing')
    yield application


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
