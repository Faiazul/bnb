from app import db
from datetime import datetime
from flask import url_for

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))  
    price = db.Column(db.Float, nullable=False, default=0.0)  
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_guests = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # active, inactive, pending, rejected
    area = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    photos = db.relationship("PropertyPhoto", back_populates="property", cascade="all, delete-orphan")
    bookings = db.relationship("Booking", back_populates="property_item", cascade="all, delete-orphan", passive_deletes=True)
    host = db.relationship("User", back_populates="hosted_properties", foreign_keys=[host_id])
    photos_rel = db.relationship('PropertyPhoto', back_populates='property', cascade="all, delete-orphan")

    def get_first_photo_url(self):
        if self.photos:
            return self.photos[0].get_url()
        return url_for('static', filename='default_property.jpg')

    def __repr__(self):
        return f"<Property {self.title}>"

class PropertyPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id', ondelete="CASCADE"))
    filename = db.Column(db.String(100))
    mimetype = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

    property = db.relationship('Property', back_populates='photos_rel')
