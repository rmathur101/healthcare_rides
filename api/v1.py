from datetime import datetime, timedelta
import logging

from flask import jsonify, request

from app import app, db
from models import Appointment, Patient, HealthcareFacility, Voucher
import statuses
from utils import generate_voucher_code

logger = logging.getLogger(__name__)

@app.route('/api/v1/create_patient/', methods=['POST'])
def create_patient():
    db.session.add(Patient())
    db.session.commit()
    return '', 200

@app.route('/api/v1/list_vouchers/', methods=['GET'])
def list_vouchers():
    vouchers = Voucher.query.all()
    vouchers = [voucher.__dict__ for voucher in vouchers]
    for voucher in vouchers:
        voucher.pop('_sa_instance_state')

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
    early_boundary = datetime.now() - timedelta(hours=app.config['EARLY_APPOINTMENT_TIME_BOUNDARY'])
    late_boundary = datetime.now() + timedelta(hours=app.config['LATE_APPOINTMENT_TIME_BOUNDARY'])

    appts = [appt.__dict__ for appt in Appointment.query.filter(
        Appointment.patient_id == patient,
        Appointment.healthcare_facility_id == hcf,
        Appointment.datetime > early_boundary,
        Appointment.datetime < late_boundary,
    ).all()]

    for appt in appts:
        appt.pop('_sa_instance_state')

    return jsonify(appts), 200

@app.route('/api/v1/checkin/', methods=['POST'])
def patient_checkin():
    appt_id = request.form['appt']

    appt = Appointment.query.get(appt_id)

    if appt:
        appt.status = statuses.PATIENT_CHECKED_IN
        db.session.add(appt)
        db.session.commit()
