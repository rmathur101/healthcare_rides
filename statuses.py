# Appointment statuses
APPOINTMENT_SCHEDULED = 0
PATIENT_CHECKED_IN = 1
APPOINTMENT_FINISHED = 2

APPOINTMENT_CODES = {
    0: 'Scheduled',
    1: 'Patient checked-in',
    2: 'Completed',
}

# Voucher statuses
VOUCHER_CREATED = 0
VOUCHER_USED = 1
VOUCHER_PAID = 2

VOUCHER_CODES = {
    0: 'Created',
    1: 'Used',
    2: 'Paid',
}

# Ride statuses
RIDE_INITIATED = 0
RIDE_IN_TRANSIT = 1
RIDE_COMPLETED = 2

RIDE_CODES = {
    0: 'Initiated',
    1: 'In transit',
    2: 'Completed',
}

PAYMENT_PENDING = 0
PAYMENT_COMPLETED = 1

PAYMENT_CODES = {
    0: 'Pending',
    1: 'Completed',
}