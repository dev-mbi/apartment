def test_add_apartment(auth):
    response = auth.post('/apartment/add', data={
        'unit_no': 'A-101',
        'floor': 1,
        'owner_name': 'John Doe',
        'owner_phone': '1234567890',
        'owner_email': 'john@test.com'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/apartment/' in response.location


def test_view_apartment_list(auth, app):
    from app import db
    from models.apartment import Apartment

    with app.app_context():
        apt = Apartment(unit_no='B-202', floor=2, owner_name='Jane')
        db.session.add(apt)
        db.session.commit()

    response = auth.get('/apartment/')
    assert response.status_code == 200
    assert b'B-202' in response.data


def test_add_complaint(auth, app):
    from app import db
    from models.apartment import Apartment

    with app.app_context():
        apt = Apartment(unit_no='C-303', floor=3)
        db.session.add(apt)
        db.session.commit()
        apt_id = apt.id

    response = auth.post('/apartment/complaints', data={
        'apartment_id': apt_id,
        'title': 'Leaky faucet',
        'description': 'Kitchen faucet is leaking'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/apartment/complaints' in response.location


def test_add_maintenance_request(auth, app):
    from app import db
    from models.apartment import Apartment

    with app.app_context():
        apt = Apartment(unit_no='D-404', floor=4)
        db.session.add(apt)
        db.session.commit()
        apt_id = apt.id

    response = auth.post('/apartment/maintenance', data={
        'apartment_id': apt_id,
        'title': 'AC not working',
        'description': 'Air conditioner stopped cooling'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/apartment/maintenance' in response.location
