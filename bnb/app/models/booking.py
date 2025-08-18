from app import db
from datetime import datetime

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete='CASCADE'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    # Relationships
    property = db.relationship("Property", back_populates="bookings")
    property_item= db.relationship('Property',back_populates='bookings')
    guest = db.relationship('User',back_populates='bookings',foreign_keys=[guest_id])
    payments = db.relationship('Payment', back_populates='booking', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Booking {self.id} for Property {self.property_id}>"
