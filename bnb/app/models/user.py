from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 
from flask_login import UserMixin
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='guest')
    profile_photo = db.Column(db.String(200))
    bio = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    hosted_properties = db.relationship('Property',back_populates='host',foreign_keys='Property.host_id',cascade='all, delete-orphan')
    bookings = db.relationship('Booking',back_populates='guest',foreign_keys='Booking.guest_id',cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    wishlist = db.relationship("Wishlist", back_populates="user", cascade="all, delete-orphan")

    def wishlist_property_ids(self):
        return [w.property_id for w in self.wishlist]
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)