def test_apartment_index_page(auth_page, live_server):
    auth_page.goto(f'{live_server}/apartment/')
    assert auth_page.locator('h1').filter(has_text='Apartment').is_visible()


def test_add_apartment(auth_page, live_server):
    auth_page.goto(f'{live_server}/apartment/add')
    auth_page.fill('input[name="unit_no"]', 'A-101')
    auth_page.fill('input[name="floor"]', '1')
    auth_page.fill('input[name="owner_name"]', 'John Doe')
    auth_page.fill('input[name="owner_phone"]', '1234567890')
    auth_page.fill('input[name="owner_email"]', 'john@test.com')
    auth_page.get_by_role('button', name='Save Apartment').click()
    assert auth_page.locator('text=Apartment added').is_visible()
    assert auth_page.locator('text=A-101').is_visible()


def test_view_apartment(auth_page, live_server):
    from models.apartment import Apartment
    from app import db

    apt = Apartment(unit_no='B-202', floor=2, owner_name='Jane Doe')
    db.session.add(apt)
    db.session.commit()
    apt_id = apt.id

    auth_page.goto(f'{live_server}/apartment/{apt_id}')
    assert auth_page.locator('text=B-202').is_visible()
    assert auth_page.locator('text=Jane Doe').is_visible()


def test_edit_apartment(auth_page, live_server):
    from models.apartment import Apartment
    from app import db

    apt = Apartment(unit_no='C-303', floor=3, owner_name='Bob')
    db.session.add(apt)
    db.session.commit()
    apt_id = apt.id

    auth_page.goto(f'{live_server}/apartment/{apt_id}/edit')
    auth_page.fill('input[name="owner_name"]', 'Bob Updated')
    auth_page.get_by_role('button', name='Update').click()
    assert auth_page.locator('text=Apartment updated').is_visible()
    assert auth_page.locator('text=Bob Updated').is_visible()


def test_delete_apartment(auth_page, live_server):
    from models.apartment import Apartment
    from app import db

    apt = Apartment(unit_no='D-404', floor=4, owner_name='To Delete')
    db.session.add(apt)
    db.session.commit()

    auth_page.goto(f'{live_server}/apartment/')
    auth_page.locator('form[action*="/delete"] button').click()
    assert auth_page.locator('text=Apartment deleted').is_visible()


def test_add_complaint(auth_page, live_server):
    from models.apartment import Apartment
    from app import db

    apt = Apartment(unit_no='E-505', floor=5, owner_name='Complainant')
    db.session.add(apt)
    db.session.commit()

    auth_page.goto(f'{live_server}/apartment/complaints')
    auth_page.locator('[name="apartment_id"]').select_option(value='1')
    auth_page.fill('input[name="title"]', 'Water leakage')
    auth_page.fill('textarea[name="description"]', 'Pipe burst in bathroom')
    auth_page.get_by_role('button', name='Submit').click()
    assert auth_page.locator('text=Complaint registered').is_visible()


def test_maintenance_request(auth_page, live_server):
    from models.apartment import Apartment
    from app import db

    apt = Apartment(unit_no='F-606', floor=6, owner_name='Maintenance Guy')
    db.session.add(apt)
    db.session.commit()

    auth_page.goto(f'{live_server}/apartment/maintenance')
    auth_page.locator('[name="apartment_id"]').select_option(value='1')
    auth_page.fill('input[name="title"]', 'AC not working')
    auth_page.fill('textarea[name="description"]', 'AC unit stopped cooling')
    auth_page.get_by_role('button', name='Submit').click()
    assert auth_page.locator('text=Maintenance request submitted').is_visible()
