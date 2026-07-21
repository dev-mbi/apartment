def test_masjid_index_page(auth_page, live_server):
    auth_page.goto(f'{live_server}/masjid/')
    assert auth_page.locator('h1').filter(has_text='Masjid Fund').is_visible()


def test_add_donation(auth_page, live_server):
    auth_page.goto(f'{live_server}/masjid/donation/add')
    auth_page.fill('input[name="amount"]', '5000')
    auth_page.fill('input[name="note"]', 'Sadaqah')
    auth_page.get_by_role('button', name='Record').click()
    assert auth_page.locator('text=Donation recorded').is_visible()


def test_add_expense(auth_page, live_server):
    auth_page.goto(f'{live_server}/masjid/expense/add')
    auth_page.fill('input[name="amount"]', '2000')
    auth_page.locator('[name="category"]').select_option('Electricity')
    auth_page.fill('textarea[name="description"]', 'Electricity bill')
    auth_page.get_by_role('button', name='Record').click()
    assert auth_page.locator('text=Expense recorded').is_visible()


def test_edit_donation(auth_page, live_server):
    from models.masjid import Donation
    from app import db

    donation = Donation(amount=1000, note='Original')
    db.session.add(donation)
    db.session.commit()
    d_id = donation.id

    auth_page.goto(f'{live_server}/masjid/donation/{d_id}/edit')
    auth_page.fill('input[name="amount"]', '2500')
    auth_page.fill('input[name="note"]', 'Updated note')
    auth_page.get_by_role('button', name='Update').click()
    assert auth_page.locator('text=Donation updated').is_visible()


def test_edit_expense(auth_page, live_server):
    from models.masjid import Expense
    from app import db

    expense = Expense(amount=500, category='Other', description='Misc')
    db.session.add(expense)
    db.session.commit()
    e_id = expense.id

    auth_page.goto(f'{live_server}/masjid/expense/{e_id}/edit')
    auth_page.fill('input[name="amount"]', '750')
    auth_page.locator('[name="category"]').select_option('Maintenance')
    auth_page.fill('textarea[name="description"]', 'Repair work')
    auth_page.get_by_role('button', name='Update').click()
    assert auth_page.locator('text=Expense updated').is_visible()


def test_delete_donation(auth_page, live_server):
    from models.masjid import Donation
    from app import db

    donation = Donation(amount=300, note='To delete')
    db.session.add(donation)
    db.session.commit()

    auth_page.goto(f'{live_server}/masjid/')
    auth_page.locator('button:has-text("Delete")').click()
    assert auth_page.locator('text=Donation deleted').is_visible()


def test_delete_expense(auth_page, live_server):
    from models.masjid import Expense
    from app import db

    expense = Expense(amount=200, category='Other', description='To delete')
    db.session.add(expense)
    db.session.commit()

    auth_page.goto(f'{live_server}/masjid/')
    auth_page.locator('button:has-text("Delete")').click()
    assert auth_page.locator('text=Expense deleted').is_visible()
