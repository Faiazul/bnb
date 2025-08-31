from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from app import db
from app.models.wishlist import Wishlist
from app.models.property import Property


wishlist_bp = Blueprint("wishlist", __name__, template_folder="templates")

# Add property to wishlist
@wishlist_bp.route("/wishlist/add/<int:property_id>", methods=["POST"])
@login_required
def add_to_wishlist(property_id):
    # Check if property already in wishlist
    existing = Wishlist.query.filter_by(user_id=current_user.id, property_id=property_id).first()
    if existing:
        flash("Property already in your wishlist!", "info")
    else:
        wishlist_item = Wishlist(user_id=current_user.id, property_id=property_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash("Added to wishlist!", "success")
    return render_template("home.html", properties=Property.query.order_by(Property.created_at.desc()).all())


# Remove property from wishlist
@wishlist_bp.route("/wishlist/remove/<int:property_id>", methods=["POST"])
@login_required
def remove_from_wishlist(property_id):
    item = Wishlist.query.filter_by(user_id=current_user.id, property_id=property_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Property removed from wishlist.", "success")
    return redirect(url_for("wishlist.view_wishlist"))

# View user's wishlist
@wishlist_bp.route("/wishlist")
@login_required
def view_wishlist():
    # Get all wishlist entries for current user
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template("wishlist.html", wishlist_items=wishlist_items)