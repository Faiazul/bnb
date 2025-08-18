from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_admin():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print("Admin already exists.")
            return

        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin_password'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        user1 = User(
            username='ohin',
            email='ohin@example.com',
            password_hash=generate_password_hash('123456'),
            is_admin=False
        )
        db.session.add(user1)
        db.session.commit()
        user2 = User(
            username='faiaz',
            email='faiaz@example.com',
            password_hash=generate_password_hash('123456'),
            is_admin=False
        )
        db.session.add(user2)
        db.session.commit()
        print("Admin user created.")

if __name__ == "__main__":
    create_admin()
