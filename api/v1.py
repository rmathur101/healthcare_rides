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

@app.route('/api/v1/appointments/', methods=['GET'])
def get_appointments():
    patient = request.args.get('patient')
    hcf = request.args.get('healthcare_facility')
    six_hours_ago = datetime.now() - timedelta(hours=6)
    six_hours_ahead = datetime.now() + timedelta(hours=6)

    appts = [appt.__dict__ for appt in Appointment.query.filter(
        Appointment.patient_id == patient,
        Appointment.healthcare_facility_id == hcf,
        Appointment.datetime < six_hours_ahead,
        Appointment.datetime > six_hours_ago
    ).all()]

    return repr(appts), 200

@app.route('/api/v1/checkin/', methods=['POST'])
def patient_checkin():
    appt_id = request.form['appt']

    appt = Appointment.query.get(appt_id)

    if appt:
        appt.status = statuses.PATIENT_CHECKED_IN
        db.session.add(appt)
        db.session.commit()
