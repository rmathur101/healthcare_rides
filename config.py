import os

class Config(object):
    DEBUG = True
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'VswAuNM838GZf/Kl)7%gensbBNk03Lolk_5btyx7lDH/Zc*b^-M7u(j2T/r#/cBuxuBhA7lkEZqzOwbr=Fol+wx1HjN7|mzFhW44'
    VOUCHER_CODE_LENGTH = 8
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/rmathur101/hackaustin/db.db'
    GOOD_DROPOFF_DISTANCE = 1500
    EARLY_APPOINTMENT_TIME_BOUNDARY = 6
    LATE_APPOINTMENT_TIME_BOUNDARY = 6
