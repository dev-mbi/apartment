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


def test_edit_apartment(auth, app):
    from app import db
    from models.apartment import Apartment

    with app.app_context():
        apt = Apartment(unit_no='E-505', floor=5, owner_name='Old Name')
        db.session.add(apt)
        db.session.commit()
        apt_id = apt.id

    response = auth.post(f'/apartment/{apt_id}/edit', data={
        'unit_no': 'E-505',
        'floor': 5,
        'owner_name': 'New Name',
        'owner_phone': '1112223333',
        'owner_email': 'new@test.com'
    }, follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        updated = db.session.get(Apartment, apt_id)
        assert updated.owner_name == 'New Name'


def test_delete_apartment(auth, app):
    from app import db
    from models.apartment import Apartment

    with app.app_context():
        apt = Apartment(unit_no='F-606', floor=6)
        db.session.add(apt)
        db.session.commit()
        apt_id = apt.id

    response = auth.post(f'/apartment/{apt_id}/delete', follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Apartment, apt_id) is None


def test_delete_complaint(auth, app):
    from app import db
    from models.apartment import Apartment, Complaint

    with app.app_context():
        apt = Apartment(unit_no='G-707', floor=7)
        db.session.add(apt)
        db.session.flush()
        c = Complaint(apartment_id=apt.id, title='Test complaint')
        db.session.add(c)
        db.session.commit()
        c_id = c.id

    response = auth.post(f'/apartment/complaints/{c_id}/delete', follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Complaint, c_id) is None


def test_create_announcement(auth, app):
    from models.apartment import Announcement

    response = auth.post('/apartment/announcements', data={
        'title': 'Test Announcement',
        'content': 'This is a test announcement'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/apartment/announcements' in response.location

    with app.app_context():
        a = Announcement.query.filter_by(title='Test Announcement').first()
        assert a is not None
        assert a.content == 'This is a test announcement'


def test_edit_announcement(auth, app):
    from app import db
    from models.apartment import Announcement

    with app.app_context():
        a = Announcement(title='Old Title', content='Old content', author_id=1)
        db.session.add(a)
        db.session.commit()
        a_id = a.id

    response = auth.post(f'/apartment/announcements/{a_id}/edit', data={
        'title': 'New Title',
        'content': 'New content'
    }, follow_redirects=False)
    assert response.status_code == 302
    assert '/apartment/announcements' in response.location

    with app.app_context():
        updated = db.session.get(Announcement, a_id)
        assert updated.title == 'New Title'
        assert updated.content == 'New content'


def test_delete_announcement(auth, app):
    from app import db
    from models.apartment import Announcement

    with app.app_context():
        a = Announcement(title='To Delete', content='Delete me', author_id=1)
        db.session.add(a)
        db.session.commit()
        a_id = a.id

    response = auth.post(f'/apartment/announcements/{a_id}/delete', follow_redirects=False)
    assert response.status_code == 302
    assert '/apartment/announcements' in response.location

    with app.app_context():
        assert db.session.get(Announcement, a_id) is None


def test_delete_maintenance(auth, app):
    from app import db
    from models.apartment import Apartment, MaintenanceRequest

    with app.app_context():
        apt = Apartment(unit_no='H-808', floor=8)
        db.session.add(apt)
        db.session.flush()
        mr = MaintenanceRequest(apartment_id=apt.id, title='Test maintenance')
        db.session.add(mr)
        db.session.commit()
        m_id = mr.id

    response = auth.post(f'/apartment/maintenance/{m_id}/delete', follow_redirects=False)
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(MaintenanceRequest, m_id) is None
