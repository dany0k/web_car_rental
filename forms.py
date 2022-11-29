import sqlite3

from flask import Flask, render_template, request, abort, flash, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError


class ClientForm(FlaskForm):
    firstname = StringField(label='Fistname')
    firstname = StringField(label='Secondname')
    firstname = StringField(label='Violation')

class CreateClientForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    firstname = StringField(label=('Firstname'),
    validators=[DataRequired(), Length(max=20)]
    )
    secondname = StringField(label=('Secondname'),
    validators=[DataRequired(), Length(max=20)]
    )
    violation=RadioField(label=('Violation'), choices=[('0', 'Missing'), ('1', 'Available')], default='0')


class EditAndDeleteClientForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    firstname = StringField(label=('Firstname'), render_kw={"placeholder": "test"},
    validators=[DataRequired(), Length(max=20)]
    )
    secondname = StringField(label=('Secondname'),
    validators=[DataRequired(), Length(max=20)]
    )
    violation=RadioField(label=('Violation'), choices=[('0', 'Missing'), ('1', 'Available')], default='0')

class VehicleForm(FlaskForm):
    firstname = StringField(label='Fistname')
    firstname = StringField(label='Secondname')
    firstname = StringField(label='Violation')


class CreateVehicleForm(FlaskForm):
    submit = SubmitField(label=('Submit'))

    firstname = StringField(label=('Firstname'),
    validators=[DataRequired(), Length(max=20)]
    )
    secondname = StringField(label=('Secondname'),
    validators=[DataRequired(), Length(max=20)]
    )
    violation=RadioField(label=('Violation'), choices=[('0', 'Missing'), ('1', 'Available')], default='0')


class EditAndDeleteVehicleForm(FlaskForm):
    submit = SubmitField(label=('Submit'))
    delete = SubmitField(label=('Delete'))

    firstname = StringField(label=('Firstname'), render_kw={"placeholder": "test"},
    validators=[DataRequired(), Length(max=20)]
    )
    secondname = StringField(label=('Secondname'),
    validators=[DataRequired(), Length(max=20)]
    )
    violation=RadioField(label=('Violation'), choices=[('0', 'Missing'), ('1', 'Available')], default='0')