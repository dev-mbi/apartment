from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func

from app import db
from models.masjid import Donation, Expense

masjid_bp = Blueprint('masjid', __name__, url_prefix='/masjid')


@masjid_bp.route('/')
@login_required
def index():
    total_donations = db.session.query(func.sum(Donation.amount)).scalar() or 0
    total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
    balance = total_donations - total_expenses
    donation_page = request.args.get('donation_page', 1, type=int)
    expense_page = request.args.get('expense_page', 1, type=int)
    donations = Donation.query.order_by(Donation.created_at.desc()).paginate(
        page=donation_page, per_page=10, error_out=False
    )
    expenses = Expense.query.order_by(Expense.created_at.desc()).paginate(
        page=expense_page, per_page=10, error_out=False
    )
    return render_template('masjid/index.html', **locals())


@masjid_bp.route('/donation/add', methods=['GET', 'POST'])
@login_required
def add_donation():
    if request.method == 'POST':
        donation = Donation(
            amount=float(request.form['amount']),
            note=request.form.get('note', '')
        )
        db.session.add(donation)
        db.session.commit()
        flash('Donation recorded', 'success')
        return redirect(url_for('masjid.index'))
    return render_template('masjid/add_donation.html')


@masjid_bp.route('/donation/<int:d_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_donation(d_id):
    donation = Donation.query.get_or_404(d_id)
    if request.method == 'POST':
        donation.amount = float(request.form['amount'])
        donation.note = request.form.get('note', '')
        db.session.commit()
        flash('Donation updated', 'success')
        return redirect(url_for('masjid.index'))
    return render_template('masjid/edit_donation.html', donation=donation)


@masjid_bp.route('/donation/<int:d_id>/delete', methods=['POST'])
@login_required
def delete_donation(d_id):
    donation = Donation.query.get_or_404(d_id)
    db.session.delete(donation)
    db.session.commit()
    flash('Donation deleted', 'success')
    return redirect(url_for('masjid.index'))


@masjid_bp.route('/expense/<int:e_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_expense(e_id):
    expense = Expense.query.get_or_404(e_id)
    if request.method == 'POST':
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']
        expense.description = request.form.get('description', '')
        db.session.commit()
        flash('Expense updated', 'success')
        return redirect(url_for('masjid.index'))
    return render_template('masjid/edit_expense.html', expense=expense)


@masjid_bp.route('/expense/<int:e_id>/delete', methods=['POST'])
@login_required
def delete_expense(e_id):
    expense = Expense.query.get_or_404(e_id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted', 'success')
    return redirect(url_for('masjid.index'))


@masjid_bp.route('/expense/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        expense = Expense(
            amount=float(request.form['amount']),
            category=request.form['category'],
            description=request.form.get('description', '')
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense recorded', 'success')
        return redirect(url_for('masjid.index'))
    return render_template('masjid/add_expense.html')
