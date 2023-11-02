import pyotp
import os

OTP_SECRET = os.getenv("OTP_SECRET")

def gen_otp():
    totp = pyotp.TOTP(OTP_SECRET)
    return totp.now()

def verify_otp(otp):
    totp = pyotp.TOTP(OTP_SECRET)
    return totp.verify(otp)