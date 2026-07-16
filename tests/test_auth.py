def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_valid_credentials(client, app):
    from app import db
    from models.user import User
    from werkzeug.security import generate_password_hash

    with app.app_context():
        user = User(
            username='testuser',
            email='test@test.com',
            password_hash=generate_password_hash('secret'),
            role='resident'
        )
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'secret'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'dashboard' in response.data


def test_login_invalid_credentials(client):
    response = client.post('/auth/login', data={
        'username': 'nobody',
        'password': 'wrong'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_page_requires_auth(client):
    response = client.get('/auth/register', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.location


def test_logout(auth):
    response = auth.get('/auth/logout', follow_redirects=False)
    assert response.status_code == 302
    assert '/auth/login' in response.location
