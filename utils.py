import string
from random import SystemRandom

from app import app
from models import Voucher


def generate_voucher_code():
    generate_a_code = True

    while generate_a_code:
        code = ''.join(SystemRandom().choice(string.ascii_uppercase) for _ in range(app.config['VOUCHER_CODE_LENGTH']))
        if Voucher.query.filter_by(code=code).first():
            continue
        return code
