# app/routes/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.models.user import User
from app.models.property import Property
from app.models.booking import Booking
from app.models.payment import Payment
from app import db
from functools import wraps
from flask import abort

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin check decorator
@admin_bp.before_request
@login_required
def restrict_to_admins():
    if not current_user.is_admin:
        abort(403) 

@admin_bp.route('/dashboard')
@login_required

def dashboard():
    users = User.query.all()
    properties = Property.query.all()
    bookings = Booking.query.all()
    payments = Payment.query.all()  
    return render_template('admin_dashboard.html', users=users, properties=properties, bookings=bookings, payments=payments)

@admin_bp.route('/delete_user/<int:user_id>')
@login_required

def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_property/<int:property_id>')
@login_required

def delete_property(property_id):

    prop = Property.query.get_or_404(property_id)
    db.session.delete(prop)
    db.session.commit()
    flash(f"Property '{prop.title}' deleted.", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_booking/<int:booking_id>')
@login_required

def delete_booking(booking_id):
    
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted.", "success")
    return redirect(url_for('admin.dashboard'))