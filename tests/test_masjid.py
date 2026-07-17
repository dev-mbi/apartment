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


def test_edit_donation(auth, app):
    from app import db
    from models.masjid import Donation

    with app.app_context():
        d = Donation(amount=5000, note='original')
        db.session.add(d)
        db.session.commit()
        d_id = d.id

    response = auth.post(f'/masjid/donation/{d_id}/edit', data={
        'amount': 7500,
        'note': 'updated'
    }, follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        updated = db.session.get(Donation, d_id)
        assert updated.amount == 7500
        assert updated.note == 'updated'


def test_delete_donation(auth, app):
    from app import db
    from models.masjid import Donation

    with app.app_context():
        d = Donation(amount=3000, note='to delete')
        db.session.add(d)
        db.session.commit()
        d_id = d.id

    response = auth.post(f'/masjid/donation/{d_id}/delete', follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Donation, d_id) is None


def test_edit_expense(auth, app):
    from app import db
    from models.masjid import Expense

    with app.app_context():
        e = Expense(amount=2000, category='Water', description='original')
        db.session.add(e)
        db.session.commit()
        e_id = e.id

    response = auth.post(f'/masjid/expense/{e_id}/edit', data={
        'amount': 2500,
        'category': 'Electricity',
        'description': 'updated'
    }, follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        updated = db.session.get(Expense, e_id)
        assert updated.amount == 2500
        assert updated.category == 'Electricity'


def test_delete_expense(auth, app):
    from app import db
    from models.masjid import Expense

    with app.app_context():
        e = Expense(amount=1500, category='Cleaning', description='to delete')
        db.session.add(e)
        db.session.commit()
        e_id = e.id

    response = auth.post(f'/masjid/expense/{e_id}/delete', follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Expense, e_id) is None
