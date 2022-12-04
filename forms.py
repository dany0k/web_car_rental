from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, RadioField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ClientsForm(FlaskForm):
    select_order = MultiCheckboxField(
        label='ID Order',
        choices=[
            (1, 'Ascending ID'),
            (2, 'Descending ID')
        ])
    select_violation = MultiCheckboxField(
        label='Violation Order',
        choices=[
            (1, 'Ascending'),
            (2, 'Descending')
        ])
    serch_name = StringField(
        label='Name'
    )
    serch_surname = StringField(
        label='Surname'
    )

    submit = SubmitField(label=('Submit'))
    status_order = 0
    status_violation = 0
    status_name = 0
    status_surname = 0


    def set_status_order(self, val):
        self.status_order = val


    def set_status_violation(self, val):
        self.status_violation = val
    
    
    def set_status_name(self, val):
        self.status_name = val


    def set_status_surname(self, val):
        self.status_surname = val
 

class CreateClientForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    firstname = StringField(
        label=('Firstname'),
        validators=[
            DataRequired(), 
            Length(max=20), 
            Regexp(regex='^([а-яА-Я]|[a-zA-Z])*$', message='Incorrent name')
        ])
    surname = StringField(
        label=('Surname'), 
        validators=[DataRequired(), 
        Length(max=20), 
        Regexp(regex='^([а-яА-Я]|[a-zA-Z])*$', message='Incorrent surname')
        ])
    violation = StringField(
        label=('Violation'),
        validators=[DataRequired(),
        Regexp('^[0-9]+$', message='Violation Amount must be a numeric value')
        ])
        

class EditAndDeleteClientForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    firstname = StringField(
        label=('Firstname'),
        validators=[DataRequired(), Length(max=20),
        Regexp(regex='^([а-яА-Я]|[a-zA-Z])*$', message='Incorrent name')])
    surname = StringField(
        label=('Surname'),
        validators=[
            DataRequired(),
            Length(max=20),
            Regexp(regex='^([а-яА-Я]|[a-zA-Z])*$', message='Incorrent surname')])
    violation = StringField(
        label=('Violation'),
        validators=[DataRequired(),
        Regexp('^[0-9]+$', message='Violation Amount must be a numeric value')
        ])


class CreateVehicleForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    vin_number = StringField(
        label='VIN',
        validators=[
            DataRequired(),
            Length(min=17, max=18),
            Regexp('^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$', message="Incorrect VIN")])
    brand = StringField(
        label='Brand',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Z0-9]+(([\',. -][a-zA-Z0-9 ])?[a-zA-Z0-9]*)*$', message='Incorrect Brand')
            ])
    price = StringField(
        label='Price',
        validators=[
            DataRequired(),
            Length(max=5),
            Regexp('^[0-9]+$', message='Price must be a numeric value')
            ])
    condition = RadioField(
        label=('Condition'),
        choices=[('0', 'Available'), ('1', 'Missing')], default='0'
        )



class EditAndDeleteVehicleForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    vin_number = StringField(
        label='VIN',
        validators=[
            DataRequired(),
            Length(min=17, max=18),
            Regexp('^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$', message="Incorrect VIN")])
    brand = StringField(
        label='Brand',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Z0-9]+(([\',. -][a-zA-Z0-9 ])?[a-zA-Z0-9]*)*$', message='Incorrect Brand')
            ])
    price = StringField(
        label='Price',
        validators=[
            DataRequired(),
            Length(max=5),
            Regexp('^[0-9]+$', message='Price must be a numeric value')
            ])
    condition = RadioField(
        label=('Condition'),
        choices=[('0', 'Available'), ('1', 'Missing')], default='0'
        )    


class CreateParkingForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    vin_number = StringField(
        label='VIN',
        validators=[
            DataRequired(),
            Length(min=17, max=18),
            Regexp('^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$', message="Incorrect VIN")
        ])


class EditAndDeleteParkingForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    vin_number = StringField(
        label='VIN',
        validators=[
            DataRequired(),
            Length(min=18, max=18),
            Regexp('^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$', message="Incorrect VIN")
        ])


class CreateRentForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    client_id = StringField(
        label='ClientID', 
        validators=[
            DataRequired(message="This field must be filled"),
            Length(min=1, max=50, message="Min length 1, Max length 50"),
            Regexp('^[0-9]+$', message='Client ID must be a numeric value')
        ])
    vin_number = StringField(
        label='VIN',
        validators=[
            DataRequired(), 
            Length(min=17, max=18),
            Regexp('^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$', message="Incorrect VIN")
            ])
    begin_date = StringField(
        label='Begin Date',
        validators=[
            DataRequired(),
            Regexp('^\s*(3[01]|[12][0-9]|0?[1-9])\/(1[012]|0?[1-9])\/((?:19|20)\d{2})\ ([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s*$', message='Invalide date format')
            ]) 
    end_date = StringField(
        label='End Date', 
        validators=[
            DataRequired(),
            Regexp('(^\s*(3[01]|[12][0-9]|0?[1-9])\/(1[012]|0?[1-9])\/((?:19|20)\d{2})\ ([0-1]?[0-9]|2[0-3]):[0-5][0-9])|IN_RENT\s*$', message='Invalide date format')
        ])


class EditAndDeleteRentForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    client_id = StringField(
        label='ClientID', 
        validators=[
            DataRequired(message="This field must be filled"),
            Length(min=1, max=50, message="Min length 1, Max length 50"),
            Regexp('^[0-9]+$', message='Client ID must be a numeric value')
        ])
    vin_number = StringField(
        label='VIN',
        validators=[
            DataRequired(), 
            Length(min=17, max=18),
            Regexp('^[A-HJ-NPR-Za-hj-npr-z\d]{8}[\dX][A-HJ-NPR-Za-hj-npr-z\d]{2}\d{6}$', message="Incorrect VIN")
            ])
    begin_date = StringField(
        label='Begin Date',
        validators=[
            DataRequired(),
            Regexp('^\s*(3[01]|[12][0-9]|0?[1-9])\/(1[012]|0?[1-9])\/((?:19|20)\d{2})\ ([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s*$', message='Invalide date format')
            ]) 
    end_date = StringField(
        label='End Date', 
        validators=[
            DataRequired(),
            Regexp('(^\s*(3[01]|[12][0-9]|0?[1-9])\/(1[012]|0?[1-9])\/((?:19|20)\d{2})\ ([0-1]?[0-9]|2[0-3]):[0-5][0-9])|IN_RENT\s*$', message='Invalide date format')
        ])
        