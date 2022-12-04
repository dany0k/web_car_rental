from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, RadioField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, NumberRange


class CreateClientForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    firstname = StringField(label=('Firstname'),
                            validators=[DataRequired(), Length(max=20)]
                            )
    surname = StringField(label=('Surname'),
                          validators=[DataRequired(), Length(max=20)]
                          )
    violation = RadioField(label=('Violation'), choices=[(
        '0', 'Missing'), ('1', 'Available')], default='0')


class EditAndDeleteClientForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    firstname = StringField(label=('Firstname'),
                            validators=[DataRequired(), Length(max=20)])
    surname = StringField(label=('Surname'),
                          validators=[DataRequired(), Length(max=20)])
    violation = RadioField(
        label=('Violation'),
        choices=[('0', 'Missing'), ('1', 'Available')],
        default='0')


class CreateVehicleForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    vin_number = StringField(label='VIN',
                             validators=[DataRequired(), Length(min=18, max=18)])
    brand = StringField(label='Brand')
    price = StringField(label='Price',
                         validators=[DataRequired(),
                         Length(max=5)]
                         )
    condition = RadioField(
        label=('Condition'),
        choices=[('0', 'Available'), ('1', 'Missing')],
        default='0')



class EditAndDeleteVehicleForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    submit = SubmitField(label=('Submit'))

    vin_number = StringField(label='VIN',
                             validators=[DataRequired(), Length(min=18, max=18)])
    brand = StringField(label='Brand')
    price = StringField(label='Price',
                         validators=[DataRequired(),
                         Length(max=5)]
                         )
    condition = RadioField(
        label=('Condition'),
        choices=[('0', 'Available'), ('1', 'Missing')],
        default='0')    


class CreateParkingForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    vin_number = StringField(label='VIN',
                             validators=[DataRequired(), Length(min=18, max=18)])


class EditAndDeleteParkingForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    vin_number = StringField(label='VIN',
                             validators=[DataRequired(), Length(min=18, max=18)])


class CreateRentForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    client_id = StringField(label='ClientID', validators=[
        DataRequired(message="This field must be filled"),
        Length(min=1, max=50, message="Min length 1, Max length 50")
    ])
    vin_number = StringField(label='VIN',
                             validators=[DataRequired(), Length(min=18, max=18)])
    begin_date = StringField(label='Begin Date',
    validators=[DataRequired()]) 
    end_date = StringField(label='End Date', 
    validators=[DataRequired()])


class EditAndDeleteRentForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    client_id = StringField(label='ClientID', validators=[
        DataRequired(message="This field must be filled"),
        Length(min=1, max=50, message="Min length 1, Max length 50")
    ])
    vin_number = StringField(label='VIN',
                             validators=[DataRequired(), Length(min=18, max=18)])
    begin_date = StringField(label='Begin Date',
    validators=[DataRequired()]) 
    end_date = StringField(label='End Date', 
    validators=[DataRequired()])