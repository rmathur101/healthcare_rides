from app import db


patient_healthcare_facilities = db.Table(
    'patient_healthcare_facilities',
    db.Column('patient_id', db.Integer, db.ForeignKey('patients.id'), primary_key=True),
    db.Column('healthcare_facility_id', db.Integer, db.ForeignKey('healthcare_facilities.id'), primary_key=True)
)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    appointments = db.relationship('Appointment', backref='patient', lazy=False)
    healthcare_facilities = db.relationship('HealthcareFacility', secondary=patient_healthcare_facilities, lazy=True)
    rides = db.relationship('Ride', backref='patient', lazy=True)
    #home = some geoloc

class HealthcareFacility(db.Model):
    __tablename__ = 'healthcare_facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    patients = db.relationship('Patient', secondary=patient_healthcare_facilities, lazy=True)
    appointments = db.relationship('Appointment', backref='healthcare_facility', lazy=True)
    #location = some geoloc

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    healthcare_facility_id = db.Column(db.Integer, db.ForeignKey('healthcare_facilities.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    voucher = db.relationship('Voucher', backref='appointment', lazy=True, uselist=False)
    #updated_by = foreign key to some User table

class Voucher(db.Model):
    __tablename__ = 'vouchers'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    ride = db.relationship('Ride', backref='voucher', lazy=True)
    code = db.Column(db.String(20))

class Ride(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    voucher_id = db.Column(db.Integer, db.ForeignKey('vouchers.id'), nullable=False)
    #driver = some foreign key to the driver?
    ride_status = db.Column(db.Integer, nullable=False)
    #pickup = some geoloc
    #dropoff = some geoloc
    cost = db.Column(db.Float, nullable=True)
    payment_status = db.Column(db.Integer, nullable=False)
