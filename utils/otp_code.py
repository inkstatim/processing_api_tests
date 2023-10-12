import pyotp


def gen_otp_data(secret):
    return {"code": f"{pyotp.TOTP(secret).now()}"}
