from app_config import app, db
from model import *
from forms import *
from flask import render_template, request, flash, redirect, url_for
from sqlalchemy import exc, desc, func
import re


def count_rows_in_table(Table):
    """Counts all rows in table"""
    return db.session.query(Table).count()


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
    elif cond == 1:
        return 2
    elif not len(is_rented) == 0:
        if is_rented[0].get_end_date() == 'IN_RENT':
            return 1
    else:
        return 0

    
def is_vin_exists(vin_number):
    """ Method returns False if there no such vin in table"""
    """ And returns True if vin exists"""
    vins = db.session.query(Vehicle)\
        .filter(Vehicle.vin_number == vin_number).one_or_none()
    if vins == None:
        return False
    else:
        return True


def check_status_checkbox(selection, Form, func):
    """Method checks what is Form status from checkbox"""
    if selection == []:
        func(Form, '0')
    if selection == ['1']:
        func(Form, '1')
    if selection == ['2']:
        func(Form, '2')


def check_status_string_field(selection, Form, func):
    """Method checks what is Form status from StringField"""
    if selection == '':
        func(Form, '0')
    else:
        func(Form, '1')


def split_str(sentence):
    """ Remove rudinant chars in string"""
    sentence = str(sentence)
    s = [int(s) for s in re.findall(r'-?\d+\.?\d*', sentence)]
    return s


def get_best_client():
    """Method returns best client ID, Name, Surname, Rents Amount """
    best_client = db.session.query(Rent.client_id, func.count(Rent.vin_number))\
    .group_by(Rent.client_id)\
        .order_by((desc(func.count(Rent.vin_number))))\
            .first()
    best_client_list = split_str(best_client)
    best_client_name = db.session.query(Client.firstname)\
        .filter(Client.client_id == best_client_list[0]).one_or_none()
    best_client_surname = db.session.query(Client.surname)\
        .filter(Client.client_id == best_client_list[0]).one_or_none()    
    best_client_name="".join(c for c in str(best_client_name) if c.isalpha())
    best_client_surname="".join(c for c in str(best_client_surname) if c.isalpha())
    best_client_list.append(best_client_name)
    best_client_list.append(best_client_surname)

    return best_client_list


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
    cur_client = db.session.query(Client)\
        .filter(Client.client_id == client_id).first()
    form = EditAndDeleteClientForm()
    # Filling form from DB using GET request
    if request.method == 'GET':
        form.firstname.data = cur_client.firstname
        form.surname.data = cur_client.surname
        form.violation.data = cur_client.violation
    # Filling DB from form using POST request
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
    

@app.route('/clients', methods=('GET', 'POST'))
def clients():
    """Select all clients from Client table"""
    form=ClientsForm()

    page = request.args.get('page', 1, type=int) 
    clients = Client.query
    
    select_order = form.select_order.data
    select_violation = form.select_violation.data
    serch_name = form.serch_name.data
    serch_surname = form.serch_surname.data  
    if request.method == 'POST':  
        page = 1
        # Check all statuses for filtering
        check_status_checkbox(select_order, ClientsForm, ClientsForm.set_status_order)
        check_status_checkbox(select_violation, ClientsForm, ClientsForm.set_status_violation)
        check_status_string_field(serch_name, ClientsForm, ClientsForm.set_status_name)
        check_status_string_field(serch_surname, ClientsForm, ClientsForm.set_status_surname)

    if ClientsForm.status_order == '0':
        form.select_order.data = []
    if ClientsForm.status_order == '1':
        clients = Client.query
        form.select_order.data = ['1']
    if ClientsForm.status_order == '2':
        clients = Client.query.order_by(desc(Client.client_id))
        form.select_order.data = ['2']

    if ClientsForm.status_violation == '0':
        form.select_violation.data = []
    if ClientsForm.status_violation == '1':
        clients = clients.order_by(Client.violation)
        form.select_violation.data = ['1']
    if ClientsForm.status_violation == '2':
        clients = clients.order_by(desc(Client.violation))
        form.select_violation.data = ['2']

    if serch_name:
        clients = clients.filter(Client.firstname == serch_name)

    if serch_surname:
        clients = clients.filter(Client.surname == serch_surname)
 
    return render_template(
        './client/clients.html',
        clients=clients.paginate(page=page, per_page=20),
        form=form)


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
            new_parking = Parking()
            form.populate_obj(new_parking)
            db.session.add(new_parking)
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
    cur_vehicle = db.session.query(Vehicle)\
        .filter(Vehicle.vin_number == vin_number).first()
    cur_parking = db.session.query(Parking)\
        .filter(Parking.vin_number == vin_number).first()
    form = EditAndDeleteVehicleForm()
    # Filling form from DB using GET request
    if request.method == 'GET':
        form.vin_number.data = cur_vehicle.vin_number
        form.brand.data = cur_vehicle.brand
        form.price.data = cur_vehicle.price
        if cur_vehicle.condition == 1:
            form.condition.default = '1'
    # Filling DB from form using POST request
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(cur_vehicle)
        if form.delete.data:
            db.session.delete(cur_vehicle)
            db.session.delete(cur_parking)
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


@app.route('/vehicles', methods=('GET', 'POST'))
def vehicles():
    """Select all vehicles from Vehicle table"""
    form=VehiclesForm()

    page = request.args.get('page', 1, type=int) 
    vehicles = Vehicle.query
    
    select_price = form.select_price.data
    select_condition = form.select_condition.data
    serch_brand = form.serch_brand.data
    serch_vin = form.serch_vin.data  
    if request.method == 'POST':  
        page = 1
        check_status_checkbox(select_price, VehiclesForm, VehiclesForm.set_status_price)
        check_status_checkbox(select_condition, VehiclesForm, VehiclesForm.set_status_condition)
        check_status_string_field(serch_brand, VehiclesForm, VehiclesForm.set_status_brand)
        check_status_string_field(serch_vin, VehiclesForm, VehiclesForm.set_status_vin)
        
    if VehiclesForm.status_price == '0':
        form.select_price.data = []
    if VehiclesForm.status_price == '1':
        vehicles = Vehicle.query
        form.select_price.data = ['1']
    if VehiclesForm.status_price == '2':
        vehicles = Vehicle.query.order_by(desc(Vehicle.price))
        form.select_price.data = ['2']

    if VehiclesForm.status_condition == '0':
        form.select_condition.data = []
    if VehiclesForm.status_condition == '1':
        vehicles = vehicles.order_by(Vehicle.condition)
        form.select_condition.data = ['1']
    if VehiclesForm.status_condition == '2':
        vehicles = vehicles.order_by(desc(Vehicle.condition))
        form.select_condition.data = ['2']

    if serch_brand:
        vehicles = vehicles.filter(Vehicle.brand == serch_brand)

    if serch_vin:
        vehicles = vehicles.filter(Vehicle.vin_number == serch_vin)
    return render_template(
        './vehicle/vehicles.html',
        vehicles=vehicles.paginate(page=page, per_page=20),
        form=form
        )


# Parking


@app.route('/create-parking', methods=('GET', 'POST'))
def create_parking():
    """Insert parking into Parking table"""
    form = CreateParkingForm()
    if request.method == 'POST' and form.validate_on_submit():  
        if is_vin_exists(form.vin_number._value()):
            new_parking = Parking()
            is_vin_parked = db.session.query(Parking.vin_number)\
                .filter(Parking.vin_number == form.vin_number._value()).one_or_none()
            if is_vin_parked != None:
                flash("This VIN arleady registered")
            else:
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
    cur_parking = db.session.query(Parking)\
        .filter(Parking.parking_id == parking_id).first()
    form = EditAndDeleteParkingForm()
    # Filling form from DB using GET request
    if request.method == 'GET':
        form.vin_number.data = cur_parking.vin_number
    # Filling DB from form using POST request
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


@app.route('/parkings', methods=('GET', 'POST'))
def parkings():
    """Select all parkings from Parking table"""
    form=ParkingsForm()

    page = request.args.get('page', 1, type=int) 
    parkings = Parking.query
    
    select_parking = form.select_parking.data
    serch_vin = form.serch_vin.data  
    if request.method == 'POST':  
        page = 1
        check_status_checkbox(select_parking, ParkingsForm, ParkingsForm.set_status_parking)
        check_status_string_field(serch_vin, ParkingsForm, ParkingsForm.set_status_parking_vin)
        
    if ParkingsForm.status_parking == '0':
        form.select_parking.data = []
    if ParkingsForm.status_parking == '1':
        parkings = Parking.query
        form.select_parking.data = ['1']
    if ParkingsForm.status_parking == '2':
        parkings = Parking.query.order_by(desc(Parking.parking_id))
        form.select_parking.data = ['2']

    if serch_vin:
        parkings = parkings.filter(Parking.vin_number == serch_vin)
    return render_template(
        './parking/parkings.html',
        parkings=parkings.paginate(page=page, per_page=20),
        form=form)


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
    cur_rent = db.session.query(Rent)\
        .filter(Rent.rent_id == rent_id).first()
    form = EditAndDeleteRentForm()
    # Filling form from DB using GET request
    if request.method == 'GET':
        form.client_id.data = cur_rent.client_id
        form.vin_number.data = cur_rent.vin_number
        form.begin_date.data = cur_rent.begin_date
        form.end_date.data = cur_rent.end_date
    # Filling DB from form using POST request
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


@app.route('/rents', methods=('GET', 'POST'))
def rents():
    """Select all rents from Rent table"""
    form=RentsForm()

    page = request.args.get('page', 1, type=int) 
    rents = Rent.query
    
    select_rent = form.select_rent.data
    select_client_id = form.select_client_id.data
    serch_vin = form.serch_vin.data
    serch_client_id = form.serch_client_id.data
    if request.method == 'POST':  
        page = 1
        check_status_checkbox(select_rent, RentsForm, RentsForm.set_status_rent)
        check_status_checkbox(select_client_id, RentsForm, RentsForm.set_status_client_id)
        check_status_string_field(serch_vin, RentsForm, RentsForm.set_status_rent_vin)
        check_status_string_field(serch_client_id, RentsForm, RentsForm.set_status_serch_client_id)
        
    if RentsForm.status_rent == '0':
        form.select_rent.data = []
    if RentsForm.status_rent == '1':
        rents = Rent.query
        form.select_rent.data = ['1']
    if RentsForm.status_rent == '2':
        rents = Rent.query.order_by(desc(Rent.rent_id))
        form.select_rent.data = ['2']

    if RentsForm.status_client_id == '0':
        form.select_client_id.data = []
    if RentsForm.status_client_id == '1':
        rents = rents.order_by(Rent.client_id)
        form.select_client_id.data = ['1']
    if RentsForm.status_client_id == '2':
        rents = rents.order_by(desc(Rent.client_id))
        form.select_client_id.data = ['2']

    if serch_client_id:
        rents = rents.filter(Rent.client_id == serch_client_id)
    if serch_vin:
        rents = rents.filter(Rent.vin_number == serch_vin)
    return render_template(
        './rent/rents.html',
        rents=rents.paginate(page=page, per_page=20),
        form=form)


@app.route('/statistics')
def statistics():
    clients_amount = count_rows_in_table(Client)
    vehicles_amount = count_rows_in_table(Vehicle)
    broken_cars = db.session.query(Vehicle)\
        .filter(Vehicle.condition == '1').count()
    working_cars = db.session.query(Vehicle)\
        .filter(Vehicle.condition == '0').count()
    parkings_amount = count_rows_in_table(Parking)
    rents_amount = count_rows_in_table(Rent)
    best_client = get_best_client()
    
    context = {
        'clients_amount' : clients_amount,
        'vehicles_amount' : vehicles_amount,
        'parkings_amount' : parkings_amount,
        'rents_amount' : rents_amount,
        'broken_cars' : broken_cars,
        'working_cars' : working_cars,
        'best_client_id' : best_client[0],
        'best_client_rents_amount' : best_client[1],
        'best_client_name' : best_client[2],
        'best_client_surname' : best_client[3]
    }

    return render_template(
        'statistics.html', **context)


@app.route('/')
def index():
    """Render index.html template"""
    return render_template('index.html')