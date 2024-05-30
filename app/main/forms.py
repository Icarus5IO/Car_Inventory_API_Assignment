from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class CarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1886)])
    color = StringField('Color', validators=[DataRequired()])
    transmission = SelectField('Transmission', choices=[('manual', 'Manual'), ('automatic', 'Automatic')], validators=[DataRequired()])
    submit = SubmitField('Add Car')
