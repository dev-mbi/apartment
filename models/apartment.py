from datetime import datetime, timezone
from app import db


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_no = db.Column(db.String(20), unique=True, nullable=False)
    floor = db.Column(db.Integer)
    owner_name = db.Column(db.String(100))
    owner_phone = db.Column(db.String(20))
    owner_email = db.Column(db.String(100))
    residents = db.relationship('Resident', backref='apartment', lazy=True)
    complaints = db.relationship('Complaint', backref='apartment', lazy=True)
    maintenance_requests = db.relationship('MaintenanceRequest', backref='apartment', lazy=True)


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    phone = db.Column(db.String(20))


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class MaintenanceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class MaintenanceBill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    society_name = db.Column(db.String(200), default='')
    month = db.Column(db.String(7), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    late_fee = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='unpaid')
    generated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    paid_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text)
    apartment = db.relationship('Apartment', backref='bills')
