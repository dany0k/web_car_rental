import sqlite3

from flask import Flask, render_template, abort, request, flash, redirect, url_for

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key'


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


############
# Clients #
############


@app.route('/<int:client_id>')
def client(client_id):
    cur_client = get_client(client_id)
    return render_template('./client/client.html', post=cur_client)


@app.route('/create-client', methods=('GET', 'POST'))
def create_client():
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


@app.route('/<int:client_id>/edit-client', methods=('GET', 'POST'))
def edit_client(client_id):
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


@app.route('/<int:client_id>/delete-client', methods=('POST',))
def delete_client(client_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM client WHERE client_id = ?', (client_id,))
    conn.commit()
    conn.close()
    flash('Client was successfully deleted!')
    return redirect(url_for('show_clients'))


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
    return render_template('./vehicle/vehiclelist.html', posts=cur_vehicle)


@app.route('/')
def index():
    return render_template('index.html')
