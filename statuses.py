# Appointment statuses
APPOINTMENT_SCHEDULED = 0
PATIENT_CHECKED_IN = 1
APPOINTMENT_FINISHED = 2

APPOINTMENT_CODES = {
    0: 'Appointment scheduled',
    1: 'Patient checked-in',
    2: 'Appointment finished',
}

# Voucher statuses
VOUCHER_CREATED = 0
VOUCHER_USED = 1
VOUCHER_PAID = 2

VOUCHER_CODES = {
    0: 'Voucher created',
    1: 'Voucher used',
    2: 'Voucher paid',
}

# Ride statuses
RIDE_INITIATED = 0
RIDE_IN_TRANSIT = 1
RIDE_COMPLETED = 2

RIDE_CODES = {
    0: 'Ride initiated',
    1: 'Ride in transit',
    2: 'Ride completed',
}

PAYMENT_PENDING = 0
PAYMENT_COMPLETED = 1

PAYMENT_CODES = {
    0: 'Payment pending',
    1: 'Payment completed',
}