def test_add_donation(auth):
    response = auth.post('/masjid/donation/add', data={
        'amount': 5000.00,
        'note': 'Monthly donation'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/masjid/' in response.location


def test_add_expense(auth):
    response = auth.post('/masjid/expense/add', data={
        'amount': 2000.00,
        'category': 'Electricity',
        'description': 'Monthly electricity bill'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/masjid/' in response.location


def test_balance_calculation(auth, app):
    from app import db
    from models.masjid import Donation, Expense

    with app.app_context():
        db.session.add(Donation(amount=10000, note='donation'))
        db.session.add(Expense(amount=3000, category='Cleaning', description='cleaning'))
        db.session.commit()

    response = auth.get('/masjid/')
    assert response.status_code == 200
    assert b'10000' in response.data or b'10000.00' in response.data
    assert b'3000' in response.data or b'3000.00' in response.data
    assert b'7000' in response.data or b'7000.00' in response.data
