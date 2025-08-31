from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.message import Message
from app.models.booking import Booking
from app.models.user import User
from app.forms.message_form import MessageForm
from sqlalchemy import or_

message_bp = Blueprint('message', __name__, template_folder='templates')

# -------------------------
# Inbox view
# -------------------------
@message_bp.route('/inbox')
@login_required
def inbox():
    """
    Display all messages sent or received by the current user, sorted by timestamp.
    """
    messages = Message.query.filter(
        or_(Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id)
    ).order_by(Message.timestamp.desc()).all()

    return render_template('messages.html', messages=messages)

# -------------------------
# Send message to admin
# -------------------------
@message_bp.route('/message/admin', methods=['GET', 'POST'])
@login_required
def message_admin():
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        flash("No admin account found.", "danger")
        return redirect(url_for('property.all_properties'))

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=admin.id,
            content=form.content.data
        )
        db.session.add(msg)
        db.session.commit()
        flash("Message sent to admin.", "success")
        return redirect(url_for('message.inbox'))

    return render_template('send_message.html', form=form, receiver=admin)

# -------------------------
# Send message between renter and owner after booking
# -------------------------
@message_bp.route('/message/booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def message_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # Determine the other user
    if current_user.id == booking.guest_id:
        other_user = booking.property.host
    elif current_user.id == booking.property.host_id:
        other_user = booking.renter
    else:
        flash("You cannot message for this booking.", "danger")
        return redirect(url_for('property.all_properties'))

    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(
            sender_id=current_user.id,
            receiver_id=other_user.id,
            content=form.content.data,
            booking_id=booking.id
        )
        db.session.add(msg)
        db.session.commit()
        flash("Message sent.", "success")
        return redirect(url_for('message.inbox'))

    return render_template('send_message.html', form=form, receiver=other_user, booking=booking)

@message_bp.route('/reply/<int:message_id>', methods=['POST'])
@login_required
def reply(message_id):
    parent_msg = Message.query.get_or_404(message_id)

    # Figure out the other user (if I’m sender, reply goes to receiver, and vice versa)
    if current_user.id == parent_msg.sender_id:
        receiver_id = parent_msg.receiver_id
    else:
        receiver_id = parent_msg.sender_id

    content = request.form.get("content")
    if not content:
        flash("Reply cannot be empty.", "danger")
        return redirect(url_for('message.inbox'))

    reply_msg = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content,
        booking_id=parent_msg.booking_id  # keep it linked to the same booking if exists
    )
    db.session.add(reply_msg)
    db.session.commit()

    flash("Reply sent.", "success")
    return redirect(url_for('message.inbox'))
