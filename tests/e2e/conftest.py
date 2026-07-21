import pytest
import threading
import time
import socket
from urllib.request import urlopen, Request
from urllib.error import URLError


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


@pytest.fixture(scope='session')
def app():
    from app import create_app
    return create_app('testing')


@pytest.fixture(scope='session')
def live_server(app):
    port = find_free_port()
    url = f'http://127.0.0.1:{port}'

    def run_server():
        app.run(port=port, debug=False, use_reloader=False)

    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    for _ in range(50):
        try:
            req = Request(url)
            urlopen(req, timeout=1)
            break
        except URLError:
            time.sleep(0.1)
    else:
        raise RuntimeError('Flask server did not start in time')

    yield url


@pytest.fixture(autouse=True)
def db(app):
    from app import db
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture
def page(context, live_server):
    p = context.new_page()
    p.set_default_timeout(10000)
    p.on('dialog', lambda dialog: dialog.accept())
    yield p
    p.close()


@pytest.fixture
def admin_user(db):
    from models.user import User
    from werkzeug.security import generate_password_hash
    user = User(
        username='admin',
        email='admin@test.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_page(page, live_server, admin_user):
    page.goto(f'{live_server}/auth/login')
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'admin123')
    page.get_by_role('button', name='Sign In').click()
    page.wait_for_url(f'{live_server}/auth/')
    return page
