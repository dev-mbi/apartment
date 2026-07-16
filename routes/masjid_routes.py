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
    donations = Donation.query.order_by(Donation.created_at.desc()).limit(10).all()
    expenses = Expense.query.order_by(Expense.created_at.desc()).limit(10).all()
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
