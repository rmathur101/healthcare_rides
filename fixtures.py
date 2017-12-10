from models import *
from utils import generate_voucher_code, verify_ride_destination
from datetime import datetime

from geopy.distance import vincenty

# You'll need to comment out `from api import v1` and `import index` from app/__init__.py to run this
# otherwise you get a circular import error

db.drop_all()
db.create_all()

patienta = Patient(first_name='Matt', last_name='Jorgenson', phone_number='5551234567', home_lat=30.332088, home_long=-97.780666)
patientb = Patient(first_name='Louise', last_name='Nelson', phone_number='5550987654', home_lat=30.297856, home_long=-97.776203)
hospitala = HealthcareFacility(name="Hospital A", lat=30.29667, long=-97.695522)
hospitalb = HealthcareFacility(name="Hospital B", lat=30.257045, long=-97.605522)
pharmacy = HealthcareFacility(name="Pharmacy", lat=30.317045, long=-97.755522)

hospitala.patients.append(patienta)
hospitala.patients.append(patientb)
hospitalb.patients.append(patientb)
pharmacy.patients.append(patienta)
pharmacy.patients.append(patientb)

appta = Appointment(patient=patienta, healthcare_facility=hospitala, datetime=datetime.now(), status=0)
apptb = Appointment(patient=patientb, healthcare_facility=hospitalb, datetime=datetime.now(), status=0)
apptc = Appointment(patient=patientb, healthcare_facility=pharmacy, datetime=datetime.now(), status=0)

vouchera = Voucher(appointment=appta, code=generate_voucher_code())
voucherb = Voucher(appointment=apptb, code=generate_voucher_code())
voucherc = Voucher(appointment=apptc, code=generate_voucher_code())

ridea = Ride(patient=patienta, voucher=vouchera, ride_status=1, payment_status=0, dropoff_lat=30.29701, dropoff_long=-97.6960)
rideb = Ride(patient=patientb, voucher=voucherb, ride_status=1, payment_status=0, dropoff_lat=30.259, dropoff_long=-97.603)
ridec = Ride(patient=patientb, voucher=voucherc, ride_status=1, payment_status=0, dropoff_lat=30.35, dropoff_long=-97.8)

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
db.session.commit()
