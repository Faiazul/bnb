from app import db
from datetime import datetime

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey("property.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    user = db.relationship("User", backref="wishlists", lazy=True)
    property = db.relationship("Property", backref="wishlists", lazy=True)

    __table_args__ = (
        db.UniqueConstraint("user_id", "property_id", name="unique_user_property_wishlist"),
    )
