from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.models.booking import Booking
from app.models.property import Property
from app.forms.booking_form import BookingForm
from app import db
from sqlalchemy import or_, and_
from app.models.payment import Payment

booking_bp = Blueprint('booking', __name__)

from sqlalchemy import and_  # no need for or_

@booking_bp.route('/property/<int:property_id>/book', methods=['GET', 'POST'])
@login_required
def book_property(property_id):
    property = Property.query.get_or_404(property_id)
    form = BookingForm()

    nights = None
    total_price = None

    if form.validate_on_submit():
        if form.check_out.data <= form.check_in.data:
            flash('Check-out date must be after check-in date', 'danger')
        else:
            nights = (form.check_out.data - form.check_in.data).days
            total_price = nights * property.price

            conflicting_bookings = Booking.query.filter(
                Booking.property_id == property_id,
                Booking.status.in_(['confirmed', 'pending']),
                Booking.check_in <= form.check_out.data,
                Booking.check_out >= form.check_in.data
            ).first()

            if conflicting_bookings:
                flash('This property is not available for the selected dates', 'danger')
            else:
                booking = Booking(
                    property_id=property_id,
                    guest_id=current_user.id,
                    check_in=form.check_in.data,
                    check_out=form.check_out.data,
                    total_price=total_price,
                    notes=form.notes.data
                )
                db.session.add(booking)
                db.session.commit()
                flash('Booking successful!', 'success')
                return redirect(url_for('booking.view_booking', booking_id=booking.id))

    elif form.check_in.data and form.check_out.data:
        nights = (form.check_out.data - form.check_in.data).days
        if nights > 0:
            total_price = nights * property.price

    return render_template(
        'book_property.html',
        form=form,
        property=property,
        nights=nights,
        total_price=total_price
    )



@booking_bp.route('/bookings/<int:booking_id>')
@login_required
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.guest_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('auth.home'))
    return render_template('view_booking.html', booking=booking)


@booking_bp.route('/bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(guest_id=current_user.id).order_by(Booking.check_in.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)


@booking_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.guest_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('auth.home'))

    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        db.session.commit()
        flash('Booking cancelled', 'success')
    else:
        flash('Cannot cancel this booking', 'danger')

    return redirect(url_for('booking.view_booking', booking_id=booking_id))

@booking_bp.route('/bookings/<int:booking_id>/pay', methods=['POST'])
@login_required
def pay_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.guest_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('auth.home'))

    # Dummy payment logic
    payment = Payment(
        booking_id=booking.id,
        amount=booking.total_price,
        status='confirmed',
    )
    db.session.add(payment)

    # ✅ Update booking status after payment
    booking.status = 'confirmed'

    try:
        db.session.commit()
        flash('Payment successful! Booking confirmed.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Payment failed: {str(e)}', 'danger')

    return redirect(url_for('booking.my_bookings'))
