from app_config import db


class Client(db.Model):
    __tablename__ = 'client'
    client_id = db.Column('client_id', db.INTEGER, primary_key=True, autoincrement=True)
    firstname = db.Column('firstname', db.Text) 
    surname = db.Column('surname', db.Text)
    violation = db.Column('violation', db.INTEGER)


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    vin_number = db.Column('vin_number', db.INTEGER, primary_key=True)
    brand = db.Column('brand', db.TEXT) 
    price = db.Column('price', db.INTEGER) 
    condition = db.Column('condition', db.INTEGER)


class Parking(db.Model):
    __tablename__ = 'parking'
    parking_id = db.Column('parking_id', db.INTEGER, primary_key=True, autoincrement=True)
    vin_number = db.Column(db.ForeignKey('vehicle.vin_number'))


class Rent(db.Model):
    __tablename__ = 'rent'
    rent_id = db.Column('rent_id', db.INTEGER, primary_key=True, autoincrement=True) 
    client_id = db.Column(db.ForeignKey('client.client_id'))
    vin_number = db.Column(db.ForeignKey('vehicle.vin_number'))
    begin_date = db.Column('begin_date', db.String(50), unique=False)
    end_date = db.Column('end_date', db.String(50), unique=False)


def get_client_id(self):
    return str(self.client_id)


def get_vin_number(self):
    return str(self.vin_number)


def get_rent_id(self):
    return str(self.rent_id)


def get_parking_id(self):
    return str(self.parking_id)
    