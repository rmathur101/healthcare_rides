from models import *
import statuses
from utils import generate_voucher_code, verify_ride_destination
from datetime import datetime

from geopy.distance import vincenty

# You'll need to comment out `from api import v1` and `import index` from app/__init__.py to run this
# otherwise you get a circular import error

db.drop_all()
db.create_all()

patienta = Patient(first_name='Matt', last_name='Jorgenson', phone_number='5551234567', home_lat=30.332088, home_long=-97.780666)
patientb = Patient(first_name='Louise', last_name='Nelson', phone_number='5550987654', home_lat=30.297856, home_long=-97.776203)
patientc = Patient(first_name='Rohan', last_name='Mathur', phone_number='5555555555', home_lat=30.276856, home_long=-97.766203)
jane = Patient(first_name='Jane', last_name='Patient', phone_number='5125551234', home_lat=30.286856, home_long=-97.746203)
hospitala = HealthcareFacility(name="Hospital A", lat=30.29667, long=-97.695522)
hospitalb = HealthcareFacility(name="Hospital B", lat=30.257045, long=-97.605522)
pharmacy = HealthcareFacility(name="Pharmacy", lat=30.317045, long=-97.755522)

hospitala.patients.append(patienta)
hospitala.patients.append(patientb)
hospitala.patients.append(jane)
hospitalb.patients.append(patientb)
hospitalb.patients.append(patientc)
hospitalb.patients.append(jane)
pharmacy.patients.append(patienta)
pharmacy.patients.append(patientb)
pharmacy.patients.append(patientc)
pharmacy.patients.append(jane)

appta = Appointment(patient=patienta, healthcare_facility=hospitala, datetime=datetime.now(), status=statuses.APPOINTMENT_FINISHED)
apptjane = Appointment(patient=jane, healthcare_facility=hospitala, datetime=datetime.now(), status=statuses.APPOINTMENT_FINISHED)
apptb = Appointment(patient=patientb, healthcare_facility=hospitalb, datetime=datetime.now(), status=statuses.APPOINTMENT_FINISHED)
apptc = Appointment(patient=patientb, healthcare_facility=pharmacy, datetime=datetime.now(), status=statuses.APPOINTMENT_SCHEDULED)
apptd = Appointment(patient=patienta, healthcare_facility=pharmacy, datetime=datetime.now(), status=statuses.APPOINTMENT_SCHEDULED)
appte = Appointment(patient=patientc, healthcare_facility=hospitalb, datetime=datetime.now(), status=statuses.PATIENT_CHECKED_IN)

vouchera = Voucher(appointment=appta, code=generate_voucher_code(), status=statuses.VOUCHER_PAID)
voucherb = Voucher(appointment=apptb, code=generate_voucher_code(), status=statuses.VOUCHER_PAID)
voucherc = Voucher(appointment=apptc, code=generate_voucher_code(), status=statuses.VOUCHER_USED)
voucherd = Voucher(appointment=apptd, code=generate_voucher_code(), status=statuses.VOUCHER_CREATED)
vouchere = Voucher(appointment=appte, code=generate_voucher_code(), status=statuses.VOUCHER_USED)

ridea = Ride(patient=patienta, voucher=vouchera, ride_status=statuses.RIDE_COMPLETED, payment_status=statuses.PAYMENT_COMPLETED, dropoff_lat=30.29701, dropoff_long=-97.6960, cost=14.56, pickup_lat=30.503784, pickup_long=-97.746326)
rideb = Ride(patient=patientb, voucher=voucherb, ride_status=statuses.RIDE_COMPLETED, payment_status=statuses.PAYMENT_PENDING, dropoff_lat=30.259, dropoff_long=-97.603, cost=19.07, pickup_lat=30.103784, pickup_long=-97.750326)
ridec = Ride(patient=patientb, voucher=voucherc, ride_status=statuses.RIDE_COMPLETED, payment_status=statuses.PAYMENT_PENDING, dropoff_lat=30.35, dropoff_long=-97.8, cost=12.89, pickup_lat=30.353784, pickup_long=-97.741326)
rided = Ride(patient=patientc, voucher=vouchere, ride_status=statuses.RIDE_COMPLETED, payment_status=statuses.PAYMENT_PENDING, dropoff_lat=30.259, dropoff_long=-97.603, cost=14.55, pickup_lat=30.403784, pickup_long=-97.738326)

# dropoff = (ridea.dropoff_lat, ridea.dropoff_long)
# hcf_location = (ridea.voucher.appointment.healthcare_facility.lat, ridea.voucher.appointment.healthcare_facility.long)
# distance = vincenty(dropoff, hcf_location).feet
# print "Ride A: {} ({})".format(verify_ride_destination(ridea), distance)
#
# dropoff = (rideb.dropoff_lat, rideb.dropoff_long)
# hcf_location = (rideb.voucher.appointment.healthcare_facility.lat, rideb.voucher.appointment.healthcare_facility.long)
# distance = vincenty(dropoff, hcf_location).feet
# print "Ride B: {} ({})".format(verify_ride_destination(rideb), distance)
#
# dropoff = (ridec.dropoff_lat, ridec.dropoff_long)
# hcf_location = (ridec.voucher.appointment.healthcare_facility.lat, ridec.voucher.appointment.healthcare_facility.long)
# distance = vincenty(dropoff, hcf_location).feet
# print "Ride C: {} ({})".format(verify_ride_destination(ridec), distance)

db.session.add(patienta)
db.session.add(patientb)
db.session.add(patientc)
db.session.commit()
