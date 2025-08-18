from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

class BookingForm(FlaskForm):
    check_in = DateField('Check-in Date', validators=[DataRequired()])
    check_out = DateField('Check-out Date', validators=[DataRequired()])
    guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])
    notes = TextAreaField('Special Requests')
    submit = SubmitField('Book Now')