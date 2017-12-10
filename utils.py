import string
from random import SystemRandom

from geopy.distance import vincenty

from app import app
from models import Voucher


def generate_voucher_code():
    generate_a_code = True

    while generate_a_code:
        code = ''.join(SystemRandom().choice(string.ascii_uppercase) for _ in range(app.config['VOUCHER_CODE_LENGTH']))
        if Voucher.query.filter_by(code=code).first():
            continue
        return code

def verify_ride_destination(ride):
    dropoff = (ride.dropoff_lat, ride.dropoff_long)
    hcf_location = (ride.voucher.appointment.healthcare_facility.lat, ride.voucher.appointment.healthcare_facility.long)

    return vincenty(dropoff, hcf_location).feet <= app.config['GOOD_DROPOFF_DISTANCE']