from datetime import datetime, timedelta
import logging

from flask import jsonify, request
from geopy.geocoders import Nominatim

from app import app, db
from models import Appointment, Patient, HealthcareFacility, Voucher
import statuses
from utils import generate_voucher_code

logger = logging.getLogger(__name__)

EARLY_BOUNDARY = datetime.now() - timedelta(hours=app.config['EARLY_APPOINTMENT_TIME_BOUNDARY'])
LATE_BOUNDARY = datetime.now() + timedelta(hours=app.config['LATE_APPOINTMENT_TIME_BOUNDARY'])


@app.route('/api/v1/create_patient/', methods=['POST'])
def create_patient():
    first_name = request.form['first_name']
    last_name = request.form['last_name'],
    phone_number = request.form['phone_number']
    geolocator = Nominatim()

    address = '{street_address}, {city}, {state} {zip}'.format(
        street_address=request.form['street_address'],
        city=request.form['city'],
        state=request.form['state'],
        zip=request.form['zip'],
    )

    location = geolocator.geocode(address)
    new_patient = Patient(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        home_lat=location.latitude,
        home_long=location.longitude,
    )

    db.session.add(new_patient)
    db.session.commit()
    return jsonify(new_patient.__dict__), 201

@app.route('/api/v1/list_vouchers/', methods=['GET'])
def list_vouchers():
    vouchers_qs = Voucher.query.all()
    vouchers = []
    for voucher in vouchers_qs:
        ride = None
        if voucher.ride:
            ride = voucher.ride.__dict__
            ride.pop('_sa_instance_state')
        voucher = voucher.__dict__
        voucher.pop('_sa_instance_state')
        appt_id = voucher.pop('appointment_id')
        appt = Appointment.query.get(appt_id).__dict__
        appt.pop('_sa_instance_state')
        voucher['appointment'] = appt
        voucher['ride'] = ride
        vouchers.append(voucher)

    return jsonify(vouchers), 200

@app.route('/api/v1/generate_voucher/', methods=['POST'])
def generate_voucher():
    patient = Patient.query.filter_by(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        phone_number=request.form['phone_number']
    ).first()

    if 'healthcare_facility' in request.form:
        hcf = HealthcareFacility.query.get(request.form['healthcare_facility'])
    else:
        hcf = HealthcareFacility.query.get(1)

    if not patient:
        response = {
            "message": "Patient does not exist.",
        }
        return jsonify(response), 404

    appt_date = datetime.strptime(request.form['apt_date'], '%m/%d/%Y')

    if appt_date < datetime.now():
        response = {
            "message": "Appointments can't be scheduled in the past.",
        }
        return jsonify(response), 400

    appointment = Appointment(
        patient=patient,
        healthcare_facility=hcf,
        datetime=appt_date,
        status=statuses.APPOINTMENT_SCHEDULED,
    )

    voucher = Voucher(
        appointment=appointment,
        code=generate_voucher_code(),
        status=statuses.VOUCHER_CREATED,
    )

    db.session.add(appointment)
    db.session.add(voucher)
    db.session.commit()

    return jsonify({
        "message": "Voucher created successfully.",
        "code": voucher.code,
    }), 201

@app.route('/api/v1/appointments/', methods=['GET'])
def get_appointments():
    patient = request.args.get('patient')
    hcf = request.args.get('healthcare_facility')

    if patient:
        appts_qs = Appointment.query.filter(
            Appointment.patient_id == patient,
            Appointment.healthcare_facility_id == hcf,
            Appointment.datetime > EARLY_BOUNDARY,
            Appointment.datetime < LATE_BOUNDARY,
        ).all()
    else:
        appts_qs = Appointment.query.filter(
            Appointment.healthcare_facility_id == hcf,
            Appointment.datetime > EARLY_BOUNDARY,
            Appointment.datetime < LATE_BOUNDARY,
        ).all()

    appts = [appt.__dict__ for appt in appts_qs]

    for appt in appts:
        appt.pop('_sa_instance_state')

    return jsonify(appts), 200

@app.route('/api/v1/check-in/', methods=['POST'])
def patient_check_in():
    patient = Patient.query.filter_by(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        phone_number=request.form['phone_number']
    ).first()

    if 'healthcare_facility' in request.form:
        hcf = HealthcareFacility.query.get(request.form['healthcare_facility'])
    else:
        hcf = HealthcareFacility.query.get(1)

    appt = patient.appointments.filter(
        Appointment.healthcare_facility == hcf,
        Appointment.datetime > EARLY_BOUNDARY,
        Appointment.datetime < LATE_BOUNDARY
    ).first()

    if appt:
        appt.status = statuses.PATIENT_CHECKED_IN
        appt.voucher.status = statuses.VOUCHER_USED
        db.session.add(appt)
        db.session.commit()
        return jsonify({
            "message": "Patient succcessfully checked-in.",
        }), 200
    else:
        return jsonify({
            "message": "No appointment found.",
        }), 404
