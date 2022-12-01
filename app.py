import sqlite3

from app_config import app, db
from model import *
from forms import *
from flask import render_template, request, abort, flash, redirect, url_for


def get_db_connection():
    conn = sqlite3.connect('./db/carrental.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_client(client_id):
    return db.session.query(Client)\
        .filter(Client.client_id == int(client_id)).one_or_none()


def get_vehicle(vin_number):
    return db.session.query(Vehicle)\
        .filter(Vehicle.vin_number == vin_number).one_or_none()


def get_parking(parking_id):
    return db.session.query(Parking)\
        .filter(Parking.parking_id == parking_id).one_or_none()


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
    cur_client = get_client(client_id)
    if cur_client is None:
        return 'Not found', 404
    return render_template(
        './client/client.html', 
        client=cur_client,
    )


@app.route('/create-client', methods=('GET', 'POST'))
def create_client():
    form = CreateClientForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        surname = form.surname.data
        violation = form.violation.data

        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            new_client = Client()
            form.populate_obj(new_client)
            db.session.add(new_client)
            db.session.commit()
            return redirect(url_for('show_clients'))
    return render_template(
        './client/create-client.html',
        form=form
        )


@app.route('/<int:client_id>/edit-client', methods=('GET', 'POST'))
def edit_client(client_id):
    cur_client = get_client(client_id)
    form = EditAndDeleteClientForm()
    if request.method == 'GET':
        form.firstname.data = cur_client.firstname
        form.surname.data = cur_client.surname
        if cur_client.violation == 1:
            form.violation.default = 1
    if request.method == 'POST' and form.validate_on_submit():
        firstname = form.firstname.data
        surname = form.surname.data
        violation = form.violation.data
        form.populate_obj(cur_client)
        if form.delete.data:
            db.session.delete(cur_client)
            db.session.commit()
            flash('Client was successfully deleted!')
            return redirect(url_for('show_clients', client_id=client_id))
        
        if not firstname or not surname or not violation:
            flash('Please fill all fields')
        else:
            form.populate_obj(cur_client)
            db.session.add(cur_client)       
            db.session.commit()
            return redirect(url_for('show_clients'))
    return render_template('./client/edit-client.html', client=cur_client, form=form)



@app.route('/client-list')
def show_clients():
    return render_template(
        './client/client-list.html'
        , clients=db.session.query(Client).all())


###########
# Vehicle #
###########


@app.route('/<string:vin_number>')
def vehicle(vin_number):
    cur_vehicle = get_vehicle(vin_number)
    if cur_vehicle is None:
        return 'Not found', 404
    return render_template(
        './vehicle/vehicle.html',
         vehicle=cur_vehicle)


@app.route('/create-vehicle', methods=('GET', 'POST'))
def create_vehicle():
    form = CreateVehicleForm()
    if request.method == 'POST' and form.validate_on_submit():
        vin_number = form.vin_number
        brand = form.brand
        price = form.price
        condition = form.condition

        if not vin_number or not brand or not price or not condition:
            flash('Please fill all fields')
        else:
            new_vehicle = Vehicle()
            form.populate_obj(new_vehicle)
            db.session.add(new_vehicle)
            db.session.commit()
            return redirect(url_for('show_vehicles'))
    return render_template(
        './vehicle/create-vehicle.html',
        form=form
    )


@app.route('/<string:vin_number>/edit-vehicle', methods=('GET', 'POST'))
def edit_vehicle(vin_number):
    cur_vehicle = get_vehicle(vin_number)
    form = EditAndDeleteVehicleForm()
    if request.method == 'GET':
        form.vin_number.data = cur_vehicle.vin_number
        form.brand.data = cur_vehicle.brand
        form.price.data = cur_vehicle.price
        if cur_vehicle.condition == 1:
            form.condition.default = '1'
    if request.method == 'POST' and form.validate_on_submit():
        vin_number = form.vin_number.data
        brand = form.brand.data
        price = form.price.data
        condition = form.condition.data
        form.populate_obj(cur_vehicle)
        if form.delete.data:
            db.session.delete(cur_vehicle)
            db.session.commit()
            flash('Vehicle was successfully deleted!')
            return redirect(url_for('show_vehicles', vin_number=vin_number))
        
        if not vin_number or not brand or not price:
            flash('Please fill all fields')
        else:
            form.populate_obj(cur_vehicle)
            db.session.add(cur_vehicle)       
            db.session.commit()
            return redirect(url_for('show_vehicles'))
    return render_template(
        './vehicle/edit-vehicle.html',
        vehicle=cur_vehicle,
        form=form)


@app.route('/vehicle-list')
def show_vehicles():
    return render_template(
        './vehicle/vehicle-list.html'
        , vehicles=db.session.query(Vehicle).all())


###########
# Parking #
###########1


@app.route('/parking/<int:parking_id>')
def parking(parking_id):
    cur_parking = get_parking(parking_id)
    if cur_parking is None:
        return 'Not found', 404
    return render_template(
        './parking/parking.html',
        parking=cur_parking)


@app.route('/create-parking', methods=('GET', 'POST'))
def create_parking():
    form = CreateParkingForm()
    if request.method == 'POST' and form.validate_on_submit():
        vin_number = form.vin_number

        if not vin_number:
            flash('Please fill all fields')
        else:
            new_parking = Parking()
            form.populate_obj(new_parking)
            db.session.add(new_parking)
            db.session.commit()
            return redirect(url_for('show_parking'))
    return render_template(
        './parking/create-parking.html',
        form=form
    )


@app.route('/parking/<int:parking_id>/edit-parking', methods=('GET', 'POST'))
def edit_parking(parking_id):
    cur_parking = get_parking(parking_id)
    form = EditAndDeleteParkingForm()
    if request.method == 'GET':
        form.vin_number.data = cur_parking.vin_number
    if request.method == 'POST' and form.validate_on_submit():
        vin_number = form.vin_number.data
        form.populate_obj(cur_parking)
        if form.delete.data:
            db.session.delete(cur_parking)
            db.session.commit()
            flash('Parking was successfully deleted!')
            return redirect(url_for('show_parking',
             vin_number=vin_number))
        
        if not vin_number:
            flash('Please fill all fields')
        else:
            form.populate_obj(cur_parking)
            db.session.add(cur_parking)       
            db.session.commit()
            return redirect(url_for('show_parking'))
    return render_template(
        './parking/edit-parking.html',
        parking=cur_parking,
        form=form)


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
    return render_template(
        './parking/parking-list.html',
         parking=db.session.query(Parking).all())


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
