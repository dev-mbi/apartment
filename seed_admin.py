from app import create_app, db
from models.user import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin created: admin / admin123')
    else:
        print('Admin already exists')
