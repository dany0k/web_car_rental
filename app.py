from app_config import app, db
from model import *
from forms import *
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import exc


def get_all_items_from_table(Table):
    """Select all items from DB`s table"""
    return db.session.query(Table).one_or_none()


def count_rows_in_table(Table):
    """Counts all rows in table"""
    return db.session.query(Table).count()


def get_client(client_id):
    """Select client from Client table by its id"""
    return db.session.query(Client)\
        .filter(Client.client_id == int(client_id)).one_or_none()


def get_vehicle(vin_number):
    """Select vehicle from Vehicle table by its id"""
    return db.session.query(Vehicle)\
        .filter(Vehicle.vin_number == vin_number).one_or_none()


def get_parking(parking_id):
    """Select parking from Parking table by its id"""
    return db.session.query(Parking)\
        .filter(Parking.parking_id == int(parking_id)).one_or_none()


def get_rent(rent_id):
    """Select rent from Rent table by its id"""
    return db.session.query(Rent)\
        .filter(Rent.rent_id == int(rent_id)).one_or_none()


def can_rent(vin_number, client_id):
    """Method check can user take the car (by VIN) in rent"""
    is_rented = db.session.query(Rent)\
        .filter(Rent.vin_number == vin_number).all()
    cond = db.session.query(Vehicle).first().get_condition()
    vins = db.session.query(Vehicle)\
        .filter(Vehicle.vin_number == vin_number).one_or_none()
    ids = db.session.query(Client)\
        .filter(Client.client_id == client_id).one_or_none()
    if vins == None:
        return 3
    elif ids == None:
        return 4
    elif cond == 0:
        return 2
    elif not len(is_rented) == 0:
        if is_rented[0].get_end_date() == 'IN_RENT':
            return 1
    else:
        return 0

    
def is_vin_exists(vin_number):
    vins = db.session.query(Vehicle)\
        .filter(Vehicle.vin_number == vin_number).one_or_none()
    if vins == None:
        return False
    else:
        return True

# Clients


@app.route('/create-client', methods=('GET', 'POST'))
def create_client():
    """Insert client into Client table"""
    form = CreateClientForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_client = Client()
        form.populate_obj(new_client)
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template(
        './client/create-client.html',
        form=form
        )


@app.route('/client/<int:client_id>/edit-client', methods=('GET', 'POST'))
def edit_client(client_id):
    """Edit client from Client table"""
    cur_client = get_client(client_id)
    form = EditAndDeleteClientForm()
    if request.method == 'GET':
        form.firstname.data = cur_client.firstname
        form.surname.data = cur_client.surname
        form.violation.data = cur_client.violation
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(cur_client)
        if form.delete.data:
            db.session.delete(cur_client)
            db.session.commit()
            flash('Client was successfully deleted!')
            return redirect(url_for('clients', client_id=client_id))
        
        form.populate_obj(cur_client)
        db.session.add(cur_client)       
        db.session.commit()
        return redirect(url_for('clients'))
    return render_template('./client/edit-client.html', client=cur_client, form=form)
    

@app.route('/clients')
def clients():
    """Select all clients from Client table"""
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=20)
    return render_template(
        './client/clients.html',
        clients=clients)


# Vehicle


@app.route('/create-vehicle', methods=('GET', 'POST'))
def create_vehicle():
    """Insert vehicle into Vehicle table"""
    form = CreateVehicleForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_vehicle = Vehicle()
            form.populate_obj(new_vehicle)
            db.session.add(new_vehicle)
            db.session.commit()
            return redirect(url_for('vehicles'))
        except exc.IntegrityError:
            flash("This VIN already exsists")
            db.session.rollback()
    return render_template(
        './vehicle/create-vehicle.html',
        form=form
    )


@app.route('/vehicle/<string:vin_number>/edit-vehicle', methods=('GET', 'POST'))
def edit_vehicle(vin_number):
    """Edit vehicle from Vehicle table"""
    cur_vehicle = get_vehicle(vin_number)
    form = EditAndDeleteVehicleForm()
    if request.method == 'GET':
        form.vin_number.data = cur_vehicle.vin_number
        form.brand.data = cur_vehicle.brand
        form.price.data = cur_vehicle.price
        if cur_vehicle.condition == 1:
            form.condition.default = '1'
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(cur_vehicle)
        if form.delete.data:
            db.session.delete(cur_vehicle)
            db.session.commit()
            flash('Vehicle was successfully deleted!')
            return redirect(url_for('vehicles', vin_number=vin_number))
        try:
            form.populate_obj(cur_vehicle)
            db.session.add(cur_vehicle)       
            db.session.commit()
            return redirect(url_for('vehicles'))
        except exc.IntegrityError:
            flash("This VIN already exsists")
            db.session.rollback()
    return render_template(
        './vehicle/edit-vehicle.html',
        vehicle=cur_vehicle,
        form=form)


@app.route('/vehicles')
def vehicles():
    """Select all vehicles from Vehicle table"""
    # Pagination
    page = request.args.get('page', 1, type=int)
    vehicles = Vehicle.query.paginate(page=page, per_page=20)
    return render_template(
        './vehicle/vehicles.html',
        vehicles=vehicles)


# Parking


@app.route('/create-parking', methods=('GET', 'POST'))
def create_parking():
    """Insert parking into Parking table"""
    form = CreateParkingForm()
    if request.method == 'POST' and form.validate_on_submit():  
        if is_vin_exists(form.vin_number._value()):
            new_parking = Parking()
            form.populate_obj(new_parking)
            db.session.add(new_parking)
            db.session.commit()
            return redirect(url_for('parkings'))
        else:
            flash("No such VIN")
    return render_template(
        './parking/create-parking.html',
        form=form
    )


@app.route('/parking/<int:parking_id>/edit-parking', methods=('GET', 'POST'))
def edit_parking(parking_id):
    """Insert parking into Parking table"""
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
            return redirect(url_for('parkings',
             vin_number=vin_number))
        
        form.populate_obj(cur_parking)
        db.session.add(cur_parking)       
        db.session.commit()
        return redirect(url_for('parkings'))
    return render_template(
        './parking/edit-parking.html',
        parking=cur_parking,
        form=form)


@app.route('/parkings')
def parkings():
    """Select all parkings from Parking table"""
    # Pagination
    page = request.args.get('page', 1, type=int)
    parkings = Parking.query.paginate(page=page, per_page=20)
    return render_template(
        './parking/parkings.html',
        parkings=parkings)


# Rent


@app.route('/create-rent', methods=('GET', 'POST'))
def create_rent():
    """Insert rent into Rent table"""
    form = CreateRentForm()
    if request.method == 'POST' and form.validate_on_submit():
        rentable = can_rent(form.vin_number._value(), form.client_id._value())
        if  rentable == 1:
            flash('This car is in rent')
        elif rentable == 2:
            flash('This car is unavailable')
        elif rentable == 3:
            flash('No such VIN')
        elif rentable == 4:
            flash('No such ClientID')
        
        else:
            new_rent = Rent()
            form.populate_obj(new_rent)
            db.session.add(new_rent)
            db.session.commit()
            return redirect(url_for('rents'))
    return render_template(
        './rent/create-rent.html',
        form=form
    )


@app.route('/rent/<int:rent_id>/edit-rent', methods=('GET', 'POST'))
def edit_rent(rent_id):
    """Edit rent from Rent table"""
    cur_rent = get_rent(rent_id)
    form = EditAndDeleteRentForm()
    if request.method == 'GET':
        form.client_id.data = cur_rent.client_id
        form.vin_number.data = cur_rent.vin_number
        form.begin_date.data = cur_rent.begin_date
        form.end_date.data = cur_rent.end_date
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(cur_rent)
        if form.delete.data:
            db.session.delete(cur_rent)
            db.session.commit()
            flash('Rent was successfully deleted!')
            return redirect(url_for('rents',
             rent_id=rent_id))
        
        form.populate_obj(cur_rent)
        db.session.add(cur_rent)       
        db.session.commit()
        return redirect(url_for('rents'))
    return render_template(
        './rent/edit-rent.html',
        rent=cur_rent,
        form=form)


@app.route('/rents')
def rents():
    """Select all rents from Rent table"""
    page = request.args.get('page', 1, type=int)
    rents = Rent.query.paginate(page=page, per_page=20)
    return render_template(
        './rent/rents.html',
        rents=rents)


@app.route('/')
def index():
    """Render index.html template"""
    return render_template('index.html')
