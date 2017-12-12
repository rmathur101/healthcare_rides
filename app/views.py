from flask import Flask, url_for, render_template, request, jsonify
from models import Appointment, Patient, HealthcareFacility, Voucher
from utils import generate_voucher_code
import statuses
from datetime import datetime, timedelta

from app import app, db

EARLY_BOUNDARY = datetime.now() - timedelta(hours=app.config['EARLY_APPOINTMENT_TIME_BOUNDARY'])
LATE_BOUNDARY = datetime.now() + timedelta(hours=app.config['LATE_APPOINTMENT_TIME_BOUNDARY'])


@app.route('/')
def root():
	return render_template("index.html")

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


@app.route('/clinic')
def clinic():
	return render_template("clinic.html")

@app.route('/dashboard')
def dashboard():
	return render_template("dashboard.html")

# @app.route("/generate_voucher", methods=["POST"])
# def generate_voucher():
# 	print request.form
# 	return "success"

@app.route('/something', methods=["POST"])
def something():
	print "something"
	return "something"


@app.route("/check_in_voucher", methods=["POST"])
def check_in_voucher():
	print request.form
	return "success"

def ccc_admin():
	return

def ride_austin_admin():
	return

