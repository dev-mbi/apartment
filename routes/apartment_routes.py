from datetime import date, datetime, timezone

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models.apartment import Apartment, Resident, Complaint, MaintenanceRequest, Announcement, MaintenanceBill
from models.user import User

apartment_bp = Blueprint('apartment', __name__, url_prefix='/apartment')


@apartment_bp.route('/')
@login_required
def index():
    q = request.args.get('q', '').strip()
    query = Apartment.query
    if q:
        query = query.filter(
            Apartment.unit_no.ilike(f'%{q}%') | Apartment.owner_name.ilike(f'%{q}%')
        )
    apartments = query.all()
    total = Apartment.query.count()
    occupied = Resident.query.count()
    pending_complaints = Complaint.query.filter_by(status='pending').count()
    pending_maintenance = MaintenanceRequest.query.filter_by(status='pending').count()
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template('apartment/index.html', **locals())


@apartment_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_apartment():
    if request.method == 'POST':
        apt = Apartment(
            unit_no=request.form['unit_no'],
            floor=request.form.get('floor', type=int),
            owner_name=request.form.get('owner_name'),
            owner_phone=request.form.get('owner_phone'),
            owner_email=request.form.get('owner_email')
        )
        db.session.add(apt)
        db.session.commit()
        flash('Apartment added', 'success')
        return redirect(url_for('apartment.index'))
    return render_template('apartment/add_apartment.html')


@apartment_bp.route('/<int:apt_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_apartment(apt_id):
    apartment = Apartment.query.get_or_404(apt_id)
    if request.method == 'POST':
        apartment.unit_no = request.form['unit_no']
        apartment.floor = request.form.get('floor', type=int)
        apartment.owner_name = request.form.get('owner_name')
        apartment.owner_phone = request.form.get('owner_phone')
        apartment.owner_email = request.form.get('owner_email')
        db.session.commit()
        flash('Apartment updated', 'success')
        return redirect(url_for('apartment.index'))
    return render_template('apartment/edit_apartment.html', apartment=apartment)


@apartment_bp.route('/<int:apt_id>/delete', methods=['POST'])
@login_required
def delete_apartment(apt_id):
    apartment = Apartment.query.get_or_404(apt_id)
    Resident.query.filter_by(apartment_id=apt_id).delete()
    Complaint.query.filter_by(apartment_id=apt_id).delete()
    MaintenanceRequest.query.filter_by(apartment_id=apt_id).delete()
    db.session.delete(apartment)
    db.session.commit()
    flash('Apartment deleted', 'success')
    return redirect(url_for('apartment.index'))


@apartment_bp.route('/<int:apt_id>')
@login_required
def view_apartment(apt_id):
    apartment = Apartment.query.get_or_404(apt_id)
    return render_template('apartment/view.html', apartment=apartment)


@apartment_bp.route('/<int:apt_id>/add-resident', methods=['GET', 'POST'])
@login_required
def add_resident(apt_id):
    apartment = Apartment.query.get_or_404(apt_id)
    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        user = User.query.get(user_id)
        if not user:
            flash('User not found', 'error')
        else:
            resident = Resident(
                user_id=user.id,
                apartment_id=apt_id,
                phone=request.form.get('phone')
            )
            db.session.add(resident)
            db.session.commit()
            flash('Resident added', 'success')
            return redirect(url_for('apartment.view_apartment', apt_id=apt_id))
    users = User.query.all()
    return render_template('apartment/add_resident.html', apartment=apartment, users=users)


@apartment_bp.route('/complaints', methods=['GET', 'POST'])
@login_required
def complaints():
    if request.method == 'POST':
        complaint = Complaint(
            apartment_id=request.form['apartment_id'],
            title=request.form['title'],
            description=request.form.get('description')
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint registered', 'success')
        return redirect(url_for('apartment.complaints'))
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    apartments = Apartment.query.all()
    return render_template('apartment/complaints.html', **locals())


@apartment_bp.route('/complaints/<int:c_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_complaint(c_id):
    complaint = Complaint.query.get_or_404(c_id)
    if request.method == 'POST':
        complaint.title = request.form['title']
        complaint.description = request.form.get('description')
        db.session.commit()
        flash('Complaint updated', 'success')
        return redirect(url_for('apartment.complaints'))
    apartments = Apartment.query.all()
    return render_template('apartment/edit_complaint.html', complaint=complaint, apartments=apartments)


@apartment_bp.route('/complaints/<int:c_id>/resolve')
@login_required
def resolve_complaint(c_id):
    complaint = Complaint.query.get_or_404(c_id)
    complaint.status = 'resolved'
    db.session.commit()
    flash('Complaint resolved', 'success')
    return redirect(url_for('apartment.complaints'))


@apartment_bp.route('/complaints/<int:c_id>/delete', methods=['POST'])
@login_required
def delete_complaint(c_id):
    complaint = Complaint.query.get_or_404(c_id)
    db.session.delete(complaint)
    db.session.commit()
    flash('Complaint deleted', 'success')
    return redirect(url_for('apartment.complaints'))


@apartment_bp.route('/maintenance', methods=['GET', 'POST'])
@login_required
def maintenance():
    if request.method == 'POST':
        mr = MaintenanceRequest(
            apartment_id=request.form['apartment_id'],
            title=request.form['title'],
            description=request.form.get('description')
        )
        db.session.add(mr)
        db.session.commit()
        flash('Maintenance request submitted', 'success')
        return redirect(url_for('apartment.maintenance'))
    requests = MaintenanceRequest.query.order_by(MaintenanceRequest.created_at.desc()).all()
    apartments = Apartment.query.all()
    return render_template('apartment/maintenance.html', **locals())


@apartment_bp.route('/maintenance/<int:m_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_maintenance(m_id):
    mr = MaintenanceRequest.query.get_or_404(m_id)
    if request.method == 'POST':
        mr.title = request.form['title']
        mr.description = request.form.get('description')
        db.session.commit()
        flash('Maintenance request updated', 'success')
        return redirect(url_for('apartment.maintenance'))
    apartments = Apartment.query.all()
    return render_template('apartment/edit_maintenance.html', mr=mr, apartments=apartments)


@apartment_bp.route('/maintenance/<int:m_id>/update/<status>')
@login_required
def update_maintenance(m_id, status):
    mr = MaintenanceRequest.query.get_or_404(m_id)
    if status in ('pending', 'in_progress', 'done'):
        mr.status = status
        db.session.commit()
        flash(f'Maintenance marked {status}', 'success')
    return redirect(url_for('apartment.maintenance'))


@apartment_bp.route('/maintenance/<int:m_id>/delete', methods=['POST'])
@login_required
def delete_maintenance(m_id):
    mr = MaintenanceRequest.query.get_or_404(m_id)
    db.session.delete(mr)
    db.session.commit()
    flash('Maintenance request deleted', 'success')
    return redirect(url_for('apartment.maintenance'))


@apartment_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    if request.method == 'POST':
        announcement = Announcement(
            title=request.form['title'],
            content=request.form['content'],
            author_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement posted', 'success')
        return redirect(url_for('apartment.announcements'))
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('apartment/announcements.html', announcements=announcements)


@apartment_bp.route('/announcements/<int:a_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_announcement(a_id):
    if current_user.role != 'admin':
        flash('Only admins can edit announcements', 'error')
        return redirect(url_for('apartment.announcements'))
    announcement = Announcement.query.get_or_404(a_id)
    if request.method == 'POST':
        announcement.title = request.form['title']
        announcement.content = request.form['content']
        db.session.commit()
        flash('Announcement updated', 'success')
        return redirect(url_for('apartment.announcements'))
    return render_template('apartment/edit_announcement.html', announcement=announcement)


@apartment_bp.route('/announcements/<int:a_id>/delete', methods=['POST'])
@login_required
def delete_announcement(a_id):
    if current_user.role != 'admin':
        flash('Only admins can delete announcements', 'error')
        return redirect(url_for('apartment.announcements'))
    announcement = Announcement.query.get_or_404(a_id)
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted', 'success')
    return redirect(url_for('apartment.announcements'))


@apartment_bp.route('/bills')
@login_required
def bills():
    month = request.args.get('month', '')
    status_filter = request.args.get('status', '')
    query = MaintenanceBill.query
    if month:
        query = query.filter(MaintenanceBill.month == month)
    if status_filter:
        query = query.filter(MaintenanceBill.status == status_filter)
    bills = query.order_by(MaintenanceBill.month.desc(), MaintenanceBill.apartment_id).all()
    apartments = Apartment.query.all()
    months = db.session.query(MaintenanceBill.month).distinct().order_by(MaintenanceBill.month.desc()).all()
    return render_template('apartment/bills.html', **locals())


@apartment_bp.route('/bills/generate', methods=['GET', 'POST'])
@login_required
def generate_bills():
    if current_user.role != 'admin':
        flash('Only admins can generate bills', 'error')
        return redirect(url_for('apartment.bills'))
    if request.method == 'POST':
        month = request.form['month']
        society_name = request.form.get('society_name', '').strip()
        amount = request.form.get('amount', type=float)
        due_date_str = request.form['due_date']
        late_fee = request.form.get('late_fee', 0, type=float)
        if not month or not amount or not due_date_str:
            flash('Month, amount, and due date are required', 'error')
            return render_template('apartment/generate_bill.html')
        apartments = Apartment.query.all()
        if not apartments:
            flash('No apartments found to generate bills for', 'error')
            return render_template('apartment/generate_bill.html')
        existing = MaintenanceBill.query.filter_by(month=month).count()
        if existing:
            flash(f'Bills for {month} already exist ({existing} found). Delete them first to regenerate.', 'error')
            return render_template('apartment/generate_bill.html', month=month, society_name=society_name, amount=amount, due_date=due_date_str, late_fee=late_fee)
        due_date = date.fromisoformat(due_date_str)
        total = amount + late_fee
        count = 0
        for apt in apartments:
            bill = MaintenanceBill(
                apartment_id=apt.id,
                society_name=society_name,
                month=month,
                amount=amount,
                late_fee=late_fee,
                total=total,
                due_date=due_date,
                status='unpaid'
            )
            db.session.add(bill)
            count += 1
        db.session.commit()
        flash(f'Generated {count} maintenance bills for {month}', 'success')
        return redirect(url_for('apartment.bills', month=month))
    return render_template('apartment/generate_bill.html')


@apartment_bp.route('/bills/<int:bill_id>')
@login_required
def view_bill(bill_id):
    bill = MaintenanceBill.query.get_or_404(bill_id)
    return render_template('apartment/print_bill.html', bill=bill)


@apartment_bp.route('/bills/<int:bill_id>/print')
@login_required
def print_bill(bill_id):
    bill = MaintenanceBill.query.get_or_404(bill_id)
    return render_template('apartment/print_bill.html', bill=bill, printable=True)


@apartment_bp.route('/bills/<int:bill_id>/pay', methods=['POST'])
@login_required
def pay_bill(bill_id):
    if current_user.role != 'admin':
        flash('Only admins can mark bills as paid', 'error')
        return redirect(url_for('apartment.bills'))
    bill = MaintenanceBill.query.get_or_404(bill_id)
    bill.status = 'paid'
    bill.paid_at = datetime.now(timezone.utc)
    db.session.commit()
    flash(f'Bill for {bill.apartment.unit_no} marked as paid', 'success')
    return redirect(url_for('apartment.view_bill', bill_id=bill.id))


@apartment_bp.route('/bills/<int:bill_id>/delete', methods=['POST'])
@login_required
def delete_bill(bill_id):
    if current_user.role != 'admin':
        flash('Only admins can delete bills', 'error')
        return redirect(url_for('apartment.bills'))
    bill = MaintenanceBill.query.get_or_404(bill_id)
    db.session.delete(bill)
    db.session.commit()
    flash('Bill deleted', 'success')
    return redirect(url_for('apartment.bills'))
