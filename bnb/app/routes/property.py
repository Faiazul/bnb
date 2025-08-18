import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.property import Property, PropertyPhoto
from app.forms.property_form import PropertyForm
from app import db
from app.routes.utils import allowed_file
from flask import current_app
from werkzeug.utils import secure_filename

property_bp = Blueprint('property', __name__, template_folder='templates')

@property_bp.route('/properties')
def all_properties():
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('home.html', properties=properties)

@property_bp.route('/properties/new', methods=['GET', 'POST'])
@login_required
def new_property():
    form = PropertyForm()
    if form.validate_on_submit():
        new_prop = Property(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            price=form.price.data,
            area=form.area.data,
            city=form.city.data,
            max_guests=form.max_guests.data,
            status=form.status.data,
            host_id=current_user.id
        )
        db.session.add(new_prop)
        db.session.flush()  # get new_prop.id before commit

        files = form.images.data
        if files:
            for i, file in enumerate(files[:5]):  # limit to 5
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    images = PropertyPhoto(
                        property=new_prop,
                        filename=filename,
                        mimetype=file.mimetype,
                        data=file.read()
                    )
                    db.session.add(images)

        db.session.commit()
        flash("Property listed successfully.", "success")
        return redirect(url_for('property.all_properties'))
    
    return render_template('new_property.html', form=form)



@property_bp.route('/property/<int:property_id>')
@login_required
def view_property(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property_details.html', property=property)

from io import BytesIO
from flask import send_file,abort

@property_bp.route('/image/<int:property_id>')
def property_image(property_id):
    property = Property.query.get_or_404(property_id)
    if not property.image_data:
        abort(404)
    return send_file(
        BytesIO(property.image_data),
        mimetype=property.image_mimetype
    ) 

@property_bp.route('/property/<int:property_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    property = Property.query.get_or_404(property_id)
    form = PropertyForm(obj=property)

    if form.validate_on_submit():
        property.title = form.title.data
        property.description = form.description.data
        property.location = form.location.data
        property.area = form.area.data
        property.city = form.city.data
        property.price = form.price.data
        property.max_guests = form.max_guests.data
        property.status = form.status.data

        files = form.images.data
        if files:
            for i, file in enumerate(files[:5]):
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    images = PropertyPhoto(
                        property=property,
                        filename=filename,
                        mimetype=file.mimetype,
                        data=file.read()
                    )
                    db.session.add(images)

        db.session.commit()
        flash('Property updated successfully!', 'success')
        return redirect(url_for('property.view_property', property_id=property.id))

    return render_template('edit_property.html', form=form, property=property)

@property_bp.route('/photo/<int:photo_id>')
def property_photo(photo_id):
    images = PropertyPhoto.query.get_or_404(photo_id)
    return send_file(BytesIO(images.data), mimetype=images.mimetype)
