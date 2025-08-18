from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.forms.login_form import LoginForm
from app import db

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('auth.home'))


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            # Redirect admin to admin dashboard
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(next_page) if next_page else redirect(url_for('auth.home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)

from app.forms.register_form import RegisterForm
from werkzeug.security import generate_password_hash

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'danger')
            return render_template('register.html', form=form)
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)



@auth_bp.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

from app.models.property import Property  

from sqlalchemy import or_, and_

@auth_bp.route('/home')
@login_required
def home():
    query = request.args.get('q', '').strip()

    if query:
        properties = Property.query.filter(
            
                or_(
                    Property.title.ilike(f"%{query}%"),
                    Property.area.ilike(f"%{query}%"),
                    Property.city.ilike(f"%{query}%")
                )
            ).all()
    else:
        properties = Property.query.all()

    return render_template('home.html', properties=properties)

