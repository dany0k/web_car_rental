import sqlite3

from app_config import app, db
from model import *
from forms import *
from flask import render_template, request, abort, flash, redirect, url_for

from sqlalchemy import create_engine, select
from sqlmodel import Session


def get_db_connection():
    conn = sqlite3.connect('./db/carrental.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_client(client_id):
    conn = get_db_connection()
    cur_client = conn.execute('SELECT * FROM client WHERE client_id=?',
                              (client_id,)).fetchone()
    conn.close()
    if cur_client is None:
        abort(404)
    return cur_client


def get_vehicle(vehicle_id):
    conn = get_db_connection()
    cur_vehicle = conn.execute('SELECT * FROM vehicle WHERE vin_number=?',
                               (vehicle_id,)).fetchone()
    conn.close()
    if cur_vehicle is None:
        abort(404)
    return cur_vehicle


def get_parking(parking_id):
    conn = get_db_connection()
    cur_parking = conn.execute('SELECT * FROM parking WHERE parking_id = ?',
                               (parking_id,)).fetchone()
    conn.close()
    if cur_parking is None:
        abort(404)
    return cur_parking


def get_rent(rent_id):
    conn = get_db_connection()
    cur_rent = conn.execute('SELECT * FROM rent WHERE rent_id = ?',
                            (rent_id,)).fetchone()
    conn.close()
    if cur_rent is None:
        abort(404)
    return cur_rent


############
# Clients #
############


@app.route('/<int:client_id>')
def client(client_id):
    cur_client = db.session.query(Client)\
        .filter(Client.client_id == int(client_id)).one_or_none()
    if cur_client is None:
        return 'Not found', 404
    return render_template(
        './client/client.html', 
        client=cur_client,
    )


@app.route('/create-client', methods=('GET', 'POST'))
def create_client():
    form = CreateClientForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        surname = form.secondname.data
        violation = form.violation.data

        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO client (firstname, surname, violation) VALUES (?, ?, ?)',
                         (firstname, surname, violation))
            conn.commit()
            conn.close()
            return redirect(url_for('show_clients'))
    return render_template('./client/create-client.html', form=form)


@app.route('/<int:client_id>/edit-client', methods=('GET', 'POST'))
def edit_client(client_id):
    cur_client = get_client(client_id)
    form = EditAndDeleteClientForm()
    form.firstname.render_kw = {"placeholder": cur_client[1]}
    form.secondname.render_kw = {"placeholder": cur_client[2]}
    if request.method == 'POST':
        if form.validate_on_submit:
            firstname = form.firstname.data
            surname = form.secondname.data
            violation = form.violation.data
            conn = get_db_connection()
            if form.delete.data:
                conn.execute(
                     'DELETE FROM client WHERE client_id = ?', (client_id,))
                conn.commit()
                conn.close()
                flash('Client was successfully deleted!')
                return redirect(url_for('show_clients'))
            
            if not firstname or not surname or not violation:
                flash('Please fill all fields')
            else:
                conn.execute('UPDATE client SET firstname = ?, surname = ?, violation = ?'
                            ' WHERE client_id = ?',
                            (firstname, surname, violation, client_id))
                conn.commit()
                conn.close()
                return redirect(url_for('show_clients'))
    return render_template('./client/edit-client.html', post=cur_client, form=form)



@app.route('/client-list')
def show_clients():
    conn = get_db_connection()
    cur_client = conn.execute('SELECT * FROM client').fetchall()
    conn.close()
    return render_template('./client/client-list.html', posts=cur_client)


###########
# Vehicle #
###########


@app.route('/<string:vin_number>')
def vehicle(vin_number):
    cur_vehicle = get_vehicle(vin_number)
    return render_template('./vehicle/vehicle.html', post=cur_vehicle)


@app.route('/create-vehicle', methods=('GET', 'POST'))
def create_vehicle():
    if request.method == 'POST':
        vin_number = request.form['vin-number']
        brand = request.form['brand']
        price = request.form['price']
        condition = request.form['condition']

        vin_number_default_len = 18
        if len(vin_number) < vin_number_default_len:
            flash('Incorrect vin number')
            return render_template('./vehicle/create-vehicle.html')
        try:
            int(price)
        except:
            flash('Incorrect price')
            return render_template('./vehicle/create-vehicle.html')

        if not vin_number or not brand or not price or not condition:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO vehicle (vin_number, brand, price, condition) VALUES (?, ?, ?, ?)',
                         (vin_number, brand, price, condition))
            conn.commit()
            conn.close()
    return render_template('./vehicle/create-vehicle.html')


@app.route('/<string:vin_number>/edit-vehicle', methods=('GET', 'POST'))
def edit_vehicle(vin_number):
    cur_vehicle = get_vehicle(vin_number)

    if request.method == 'POST':
        vin_num = request.form['vin-number']
        brand = request.form['brand']
        price = request.form['price']
        condition = request.form['condition']

        if not vin_num or not brand or not price or not condition:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE vehicle SET vin_number = ?, brand = ?, price = ?, condition = ?'
                         ' WHERE vin_number = ?',
                         (vin_num, brand, price, condition, vin_num))
            conn.commit()
            conn.close()
            return redirect(url_for('show_vehicles'))

    return render_template('./vehicle/edit-vehicle.html', post=cur_vehicle)


@app.route('/<string:vin_number>/delete-vehicle', methods=('POST',))
def delete_vehicle(vin_number):
    conn = get_db_connection()
    conn.execute('DELETE FROM vehicle WHERE vin_number = ?', [vin_number])
    conn.commit()
    conn.close()
    flash('Vehicle was successfully deleted!')
    return redirect(url_for('show_vehicles'))


@app.route('/vehicle-list')
def show_vehicles():
    conn = get_db_connection()
    cur_vehicle = conn.execute('SELECT * FROM vehicle').fetchall()
    conn.close()
    return render_template('./vehicle/vehicle-list.html', posts=cur_vehicle)


###########
# Parking #
###########1


@app.route('/parking/<int:parking_id>')
def parking(parking_id):
    cur_parking = get_parking(parking_id)
    return render_template('./parking/parking.html', post=cur_parking)


@app.route('/create-parking', methods=('GET', 'POST'))
def create_parking():
    conn = get_db_connection()
    if request.method == 'POST':
        vin_number = request.form['vin_number']
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        vins_list = c.execute('SELECT vin_number FROM parking').fetchall()
        for i in range(len(vins_list)):
            if vins_list[i] != vin_number and i == len(vins_list) - 1:
                flash('This VIN number is not exist.')
                return render_template('./parking/create-parking.html')
            elif vins_list[i] == vin_number:
                break
        if not vin_number:
            flash('Please fill all fields')
        else:
            conn.execute('INSERT INTO parking (vin_number) VALUES (?)',
                         [vin_number])
            conn.commit()
            conn.close()
    return render_template('./parking/create-parking.html')


@app.route('/parking/<int:parking_id>/edit-parking', methods=('GET', 'POST'))
def edit_parking(parking_id):
    cur_parking = get_parking(parking_id)

    if request.method == 'POST':
        conn = get_db_connection()
        vin_number = request.form['vin_number']
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        vins_list = c.execute('SELECT vin_number FROM parking').fetchall()
        for i in range(len(vins_list)):
            if vins_list[i] != vin_number and i == len(vins_list) - 1:
                flash('This VIN number is not exist.')
                return render_template('./parking/edit-parking.html', post=cur_parking)
            elif vins_list[i] == vin_number:
                break
        if not vin_number:
            flash('Please fill all fields')
        else:
            conn.execute('UPDATE parking SET vin_number = ?'
                         ' WHERE parking_id = ?',
                         (vin_number, parking_id))
            conn.commit()
            conn.close()
            return redirect(url_for('show_parking'))

    return render_template('./parking/edit-parking.html', post=cur_parking)


@app.route('/parking/<int:parking_id>/delete-parking', methods=('POST',))
def delete_parking(parking_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM parking WHERE parking_id = ?', (parking_id,))
    conn.commit()
    conn.close()
    flash('Parking was successfully deleted!')
    return redirect(url_for('show_parking'))


@app.route('/parking-list')
def show_parking():
    conn = get_db_connection()
    cur_parking = conn.execute('SELECT * FROM parking').fetchall()
    conn.close()
    return render_template('./parking/parking-list.html', posts=cur_parking)


########
# Rent #
########


@app.route('/rent/<int:rent_id>')
def rent(rent_id):
    cur_rent = get_rent(rent_id)
    return render_template('./rent/rent.html', post=cur_rent)


@app.route('/create-rent', methods=('GET', 'POST'))
def create_rent():
    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        violation = request.form['violation']

        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO client (firstname, surname, violation) VALUES (?, ?, ?)',
                         (firstname, surname, violation))
            conn.commit()
            conn.close()
    return render_template('./client/create-client.html')


@app.route('/rent/<int:rent_id>/edit-rent', methods=('GET', 'POST'))
def edit_rent(client_id):
    cur_client = get_client(client_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        surname = request.form['surname']
        violation = request.form['violation']

        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE client SET firstname = ?, surname = ?, violation = ?'
                         ' WHERE client_id = ?',
                         (firstname, surname, violation, client_id))
            conn.commit()
            conn.close()
            return redirect(url_for('show_clients'))

    return render_template('./client/edit-client.html', post=cur_client)


@app.route('/rent/<int:rent_id>/delete-rent', methods=('POST',))
def delete_rent(client_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM client WHERE client_id = ?', (client_id,))
    conn.commit()
    conn.close()
    flash('Client was successfully deleted!')
    return redirect(url_for('show_clients'))


@app.route('/rent-list')
def show_rent():
    conn = get_db_connection()
    cur_rent = conn.execute('SELECT * FROM rent').fetchall()
    conn.close()
    return render_template('./rent/rent-list.html', posts=cur_rent)


@app.route('/')
def index():
    return render_template('index.html')
