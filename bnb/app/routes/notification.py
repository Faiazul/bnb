from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.notification import Notification

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/notifications')
@login_required
def view_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id)\
                                      .order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifications)
