def test_login_page_loads(page, live_server):
    page.goto(f'{live_server}/auth/login')
    assert page.locator('h2').filter(has_text='Welcome Back').is_visible()
    assert page.locator('input[name="username"]').is_visible()
    assert page.locator('input[name="password"]').is_visible()


def test_login_success(page, live_server):
    from models.user import User
    from werkzeug.security import generate_password_hash
    from app import db

    user = User(
        username='testuser',
        email='test@test.com',
        password_hash=generate_password_hash('secret'),
        role='resident'
    )
    db.session.add(user)
    db.session.commit()

    page.goto(f'{live_server}/auth/login')
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password"]', 'secret')
    page.get_by_role('button', name='Sign In').click()
    page.wait_for_url(f'{live_server}/auth/')
    assert page.locator('h1').filter(has_text='Dashboard').is_visible()


def test_login_invalid_credentials(page, live_server):
    page.goto(f'{live_server}/auth/login')
    page.fill('input[name="username"]', 'nobody')
    page.fill('input[name="password"]', 'wrong')
    page.get_by_role('button', name='Sign In').click()
    assert page.locator('text=Invalid username or password').is_visible()


def test_logout(auth_page, live_server):
    auth_page.click('text=Logout')
    auth_page.wait_for_url(f'{live_server}/auth/login')
    assert auth_page.locator('h2').filter(has_text='Welcome Back').is_visible()


def test_register_page_requires_login(page, live_server):
    page.goto(f'{live_server}/auth/register')
    assert page.url.startswith(f'{live_server}/auth/login')


def test_register_user(auth_page, live_server):
    auth_page.goto(f'{live_server}/auth/register')
    auth_page.fill('input[name="username"]', 'newuser')
    auth_page.fill('input[name="email"]', 'new@test.com')
    auth_page.fill('input[name="password"]', 'newpass123')
    auth_page.select_option('select[name="role"]', 'resident')
    auth_page.get_by_role('button', name='Register').click()
    assert auth_page.locator('text=User created successfully').is_visible()
