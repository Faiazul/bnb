from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms.edit_profile_form import EditProfileForm
from app.forms.change_password_form import ChangePasswordForm
from app import db
from werkzeug.security import check_password_hash, generate_password_hash

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
@login_required
def view_profile():
    return render_template('view_profile.html')

@profile_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('profile.view_profile'))
    return render_template('edit_profile.html', form=form)

@profile_bp.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated.', 'success')
            return redirect(url_for('profile.view_profile'))
    return render_template('change_password.html', form=form)